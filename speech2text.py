import speech_recognition as sr
# import csv

def audio():
	r = sr.Recognizer()
	text = ""

	with sr.Microphone() as source:
		print("Talk")
		audio_text = r.listen(source)
		print("Time over, thanks")
		try:
			# using google speech recognition
			text = r.recognize_google(audio_text)
			print("Text: "+ text)

			# with open("conversation.csv","a") as f:
			# 	writer = csv.writer(f)
			# 	writer.writerow([text])
		except:
			print("Sorry, I did not get that")
	return text

# def main():
# 	with open("conversation.csv","w") as f:
# 		writer = csv.writer(f)
# 		writer.writerow(["Conversation"])

# 	audio()

# if __name__== "__main__":
# 	main()