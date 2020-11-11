import pyttsx3

def t2s(text):
	engine = pyttsx3.init()
	engine.save_to_file(text,'t2s.mp3')
	print("File saved")
	engine.runAndWait()	

	