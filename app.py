# import flask
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, BertForNextSentencePrediction, BertTokenizer
from fetch_google import *
# from fetch_context import *
from qnautils import *
from speech2text import *
import gpt_2_simple as gpt2
import tensorflow as tf

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
	# context = get_context_from_data(query,df)
	# print(context)
	# answers = Fetching_answers([query],df,model,tokenizer)
	answers = phase_one_end([query],df,model,tokenizer)
	GPT2_generation = regeneration("When did you start liking science?",words,model_nsp,tokenizer_nsp,sess)
	# lsprint(answers)

if __name__ == '__main__':
    # app.run()
    main()