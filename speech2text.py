import speech_recognition as sr
# import csv

def audio():
	r = sr.Recognizer()
	text = ""
	filename = "/content/Kalam-AI/recording.wav"
	with sr.AudioFile(filename) as source:
		# listen for the data (load audio to memory)
		audio_data = r.record(source)
		# recognize (convert from speech to text)
		text = r.recognize_google(audio_data)
		print(text)
	return text
