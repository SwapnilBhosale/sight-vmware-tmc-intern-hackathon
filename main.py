
import time
from threading import Lock, Thread

import brain
import speak
import speech_recognition as sr
import speech_to_text


class WebcamVideoStream :
    def __init__(self, src = 0, width = 320, height = 240) :
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self) :
        if self.started :
            print "already started!!"
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) :
        while self.started :
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self) :
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self) :
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()

def main():
    
    time.sleep(2)
    recognizer = sr.Recognizer()  
    while 1:
        #get the trigger using text to speech
        try: 
            with sr.Microphone() as source: 
                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level  
                recognizer.adjust_for_ambient_noise(source, duration=0.2) 
                audio = recognizer.listen(source) 
                my_text = recognizer.recognize_google(audio)
                if len(my_text) > 0:
                    brain.brain(my_text)

    
if __name__ == '__main__':
    main()
