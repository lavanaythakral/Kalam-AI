from transformers import AutoTokenizer, AutoModelForQuestionAnswering, BertForNextSentencePrediction, BertTokenizer
# import gpt_2_simple as gpt2

tokenizer_qa = AutoTokenizer.from_pretrained("deepset/bert-large-uncased-whole-word-masking-squad2")
model_qa = AutoModelForQuestionAnswering.from_pretrained("deepset/bert-large-uncased-whole-word-masking-squad2")

print("BERT For Q/A downloaded")

model_nsp = BertForNextSentencePrediction.from_pretrained('bert-base-cased')
tokenizer_nsp = BertTokenizer.from_pretrained('bert-base-cased')

print("BERT NSP downloaded")

# sess = gpt2.start_tf_sess()
# gpt2.load_gpt2(sess, run_name='run1_topical_token')

# print("GPT2 loaded")