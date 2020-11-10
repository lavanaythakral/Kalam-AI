from nltk import wordpunct_tokenize, WordNetLemmatizer, sent_tokenize, pos_tag
from nltk.corpus import stopwords as sw, wordnet as wn
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def convert_data(sentences):
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(sentences)
	X = normalize(X)
	print("Data vectorization completed\n")
	return X

def get_context(query,X,data_sentences):
	vectorizer = TfidfVectorizer(stop_words='english')
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
			temp = temp + data_sentences[i]
			# if(i+1 < len(data_sentences)):
			#   temp = temp + data_sentences[i+1]

	print("Context has been extracted\n")
	return temp

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
			temp = temp + data_sentences[i]
			# if(i+1 < len(data_sentences)):
			#   temp = temp + data_sentences[i+1]

	print("Context has been extracted\n")
	return context

