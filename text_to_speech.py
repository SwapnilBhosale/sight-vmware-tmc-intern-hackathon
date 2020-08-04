import pyttsx3


# Text to Voice
def SpeakText(words): 
    engine = pyttsx3.init() 
    engine.say(words)  
    engine.runAndWait()
