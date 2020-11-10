import gpt_2_simple as gpt2
from torch.nn.functional import softmax
from transformers import BertForNextSentencePrediction,BertTokenizer
from qnautils import *
from fetch_google import *
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
import re

def generate_candidates(input,sess):
	print("GPT2 generating for :",input)
	generated_text = gpt2.generate(sess,
		length=100,
		run_name='run1_topical_token',
		return_as_list=True,
		temperature=0.7,
		prefix=input,
		nsamples=15,
		truncate = '.',
		batch_size=5,
		top_k = 5,
		include_prefix = False)

	def clean(input_st, sub):
		return input_st.replace(sub, '').lstrip()

	cleaned = []
	for text in generated_text:
		cleaned.append(re.sub(r"^\W+", "",clean(text,'<|endoftext|>')))

	return cleaned


def top_result(seq_A,seq_B,model,tokenizer):
	# print(seq_B)
	response = seq_B[0]
	max_prob = -1
	for seq in seq_B:
		encoded = tokenizer.encode_plus(seq_A, text_pair=seq, return_tensors='pt')
		seq_relationship_logits = model(**encoded)[0]
		probs = softmax(seq_relationship_logits, dim=1)
		if probs[0][0] > max_prob:
			max_prob = probs[0][0]
			response = seq
		if max_prob >= 0.97:
			return response
	else:
		return -1


def master_GPT2(inp,model,tokenizer,sess):
  generation_cleaned = generate_candidates(inp,sess)
  # print(generate)
  # generation_cleaned = []
  # # print(generate)
  # for gen in generate[5:14:2]:
  #   generation_cleaned.append(re.sub(r"^\W+", "",clean(clean(gen,inp),'<|endoftext|>')))
  
  # print(generation_cleaned)
  candidates = []
  for gen in generation_cleaned:
    if len(ner(gen)) == 0:
      # print(gen)
      candidates.append(gen)
  print(candidates)
  
  res = top_result(inp,candidates,model,tokenizer)
  polarity = sid.polarity_scores(res)['compound']
  # print(res)
  # print(polarity)
  return res,polarity

def regeneration(inp,words,model,tokenizer,sess):
  flg = 1
  resp = ""
  pol = ""
  
  while(flg == 1):
    flg = 0
    resp,pol = master_GPT2(inp,model,tokenizer,sess)
    txt,keywords = keys(resp)
    print(resp,pol)
    if pol > 0.0:
      polarity = 'positive'
    elif pol < 0.0:
      polarity = 'negative'
    else:
      polarity = 'neutral'
    for x in keywords:
      if x in words.keys() and polarity != words[x]:
        flg = 1
  return resp
