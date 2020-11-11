import pyttsx3

def t2s(text):
	engine = pyttsx3.init()
	engine.setProperty('rate', 100)
	engine.setProperty('voice','hindi')
	engine.save_to_file(text,'Wav2Lip/data/t2s.mp3')
	# print("File saved")
	engine.runAndWait()	

