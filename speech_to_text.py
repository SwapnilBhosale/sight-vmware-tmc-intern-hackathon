# Python program to translate 
# speech to text and text to speech 

from speech_recognition import *
import speech_recognition as sr 
import pyttsx3

recognizer = sr.Recognizer()  

# Text to Voice
def SpeakText(words): 
    engine = pyttsx3.init() 
    engine.say(words)  
    engine.runAndWait() 

# Voice To Text
while(1):     
    try: 
        with sr.Microphone() as source: 
            # wait for a second to let the recognizer 
            # adjust the energy threshold based on 
            # the surrounding noise level  
            recognizer.adjust_for_ambient_noise(source, duration=0.2) 
            print("say something ") 
              
            audio = recognizer.listen(source) 
            my_text = recognizer.recognize_google(audio)
            print("Did you say "+ my_text.lower()) 
              
    except sr.RequestError as e: 
        print("Could not request results; {0}".format(e)) 
    except sr.UnknownValueError: 
        print("unknown error occured") 

