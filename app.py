# import flask
import tensorflow as tf
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, BertForNextSentencePrediction, BertTokenizer
from fetch_google import *
# from fetch_context import *
from qnautils import *
from speech2text import *
import gpt_2_simple as gpt2
from improvutils import *
import re
from termcolor import colored
import pyttsx3
from text2speech import *

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, run_name='run1_topical_token')

print("GPT2 loaded")

tokenizer = AutoTokenizer.from_pretrained("deepset/bert-large-uncased-whole-word-masking-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("deepset/bert-large-uncased-whole-word-masking-squad2")

print("BERT For Q/A downloaded")

model_nsp = BertForNextSentencePrediction.from_pretrained('bert-base-cased')
tokenizer_nsp = BertTokenizer.from_pretrained('bert-base-cased')

print("BERT NSP downloaded")

words = {'science' : 'positive'}

# app = flask.Flask(__name__, template_folder='templates')
# @app.route('/')
def main():
		# return(flask.render_template('main.html'))
	df = get_data()
	query = audio()
	# query = "When did you start liking science?"
	context = get_context_from_data(query,df)
	# print(context)
	answers = Fetching_answers([query],df,model,tokenizer)
	answers = phase_one_end([query],df,model,tokenizer)
	improv_return = ""
	if(answers[0] == 'GPT2' or answers[0] == 'PASS'):
		GPT2_generation = regeneration(query,words,model_nsp,tokenizer_nsp,sess)
		print(GPT2_generation)
		improv_return = GPT2_generation
	else:
		print(answers[0])
		improv_return = answers[0]
	# print(colored(GPT2_generation,"green"))
	# lsprint(answers)
	t2s(improv_return)
	return t2s
	
if __name__ == '__main__':
		# app.run()
		main()
