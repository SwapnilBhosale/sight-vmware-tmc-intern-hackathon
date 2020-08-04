# Python program to translate 
# speech to text and text to speech 

#from speech_recognition import *
import speech_recognition as sr
import pyttsx3
from cv2 import cv2
import subprocess

def TakePicture():
    cam = cv2.VideoCapture(0)
    print(cam)

    cv2.namedWindow("test")

    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            command = './darknet detect cfg/yolov3.cfg yolov3.weights opencv_frame_{}.jpg'.format(img_counter)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            process.wait()
            output = process.stdout.read().decode("utf-8")

            useful_info = output.split('\n')[1:-1]
            items = [item_str.split(':')[0] for item_str in useful_info]
            print(items)
            for item in items:
                SpeakText(item)
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

# Text to Voice
def SpeakText(words): 
    engine = pyttsx3.init() 
    engine.say(words)  
    engine.runAndWait()

def SpeechToText():
    recognizer = sr.Recognizer()  
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
            if "describe" in my_text.lower():
                TakePicture()
                
    except sr.RequestError as e: 
        print("Could not request results; {0}".format(e)) 
    except sr.UnknownValueError: 
        print("unknown error occured")     

if __name__ == "__main__":
    # Voice To Text
    SpeechToText()
