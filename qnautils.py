import torch
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk import wordpunct_tokenize, WordNetLemmatizer, sent_tokenize, pos_tag
from nltk.corpus import stopwords as sw, wordnet as wn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import spacy
nlp = spacy.load("en_core_web_sm")
from fetch_google import *

def get_data():
  df = pd.read_csv('WOF_split_into_sentences.csv')
  sentences = list(df['Sentences'])
  print("Number of sentences in the dataframe : ",len(sentences))
  return df

def get_context_from_data(query,df):
  sentences = list(df['Sentences'])
  vectorizer = TfidfVectorizer(stop_words='english')
  X = vectorizer.fit_transform(sentences)
  X = normalize(X)
  print("Data vectorization completed\n")
  
  Question = vectorizer.transform([query])
  Question = normalize(Question)
  cosineSimilarities = cosine_similarity(Question, X).flatten()
  idx = cosineSimilarities.argsort()[::-1][:20]
  temp = ""
  # print(query)
  for i in idx:                                                                             
    if(cosineSimilarities[i] != 0):
      # if(i-1 >=0):
      #   temp = temp + data_sentences[i-1]
      temp = temp + sentences[i]
      # if(i+1 < len(data_sentences)):                                                                              
      #   temp = temp + data_sentences[i+1]

  print("Context has been extracted\n")
  return temp

def qna(questions,df,model,tokenizer):
  answers = []
  for question in questions:
    print("Looking for answer for question : ", question)
    text = get_context_from_data(question,df)
    inputs = tokenizer(question, text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]
    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer_start_scores, answer_end_scores = model(**inputs)
    answer_start = torch.argmax(answer_start_scores)  # Get the most likely beginning of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print("Answer found\n")
    answers.append(answer)
  return answers

def Fetching_answers(test_questions,df,model,tokenizer):
  answers = qna(test_questions,df,model,tokenizer)
  for idx,ans in enumerate(answers):
    if ans == '[CLS]' or ans == '':
      res = master(test_questions[idx])
      if res == 'No clue':
        answers[idx] = 'PASS' 
      else:
        answers[idx] = res
  return answers


def ner(sentence):
  doc = nlp(sentence)
  entities = []
  for ent in doc.ents:
    entities.append([ent.text,ent.label_])
  return entities

def entities(sentences,answers):
  for idx,sen in enumerate(sentences):
    if(answers[idx] == 'PASS' and len(ner(sen)) == 0):
      print(sen)
      answers[idx] = 'GPT2'
  return answers

def phase_one_end(questions,df,model,tokenizer):
  ans = Fetching_answers(questions,df,model,tokenizer)
  final = entities(questions,ans)
  return final
