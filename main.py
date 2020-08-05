import argparse
import subprocess
import time
from threading import Lock, Thread

import brain
import cv2
import image_detection_yolo as yolo
import speech_recognition as sr
import text_to_speech

parser = argparse.ArgumentParser()
parser.add_argument('--webcam', help="Y/N", default="Y")
args = parser.parse_args()

class camThread(Thread):
    def __init__(self, previewName, camID):
        Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:

        height, width, channels = frame.shape
        blob, outputs = yolo.detect_objects(frame, model, output_layers)
        boxes, confs, class_ids = yolo.get_box_dimensions(outputs, height, width)
        yolo.draw_labels(boxes, confs, colors, class_ids, classes, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(1)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


def main():

    recognizer = sr.Recognizer() 
    model, classes, colors, output_layers = yolo.load_yolo() 
    time.sleep(2)
    #model, classes, colors, output_layers = yolo.load_yolo()
    #thread1 = camThread("Camera 1", 0)
    #thread1.start()
    print("*** args: ",args)
    if args.webcam == "Y":
        subprocess.Popen(["python3", "image_detection_yolo.py"], close_fds=True)
    else:
        subprocess.Popen(["python3", "image_detection_yolo.py", "--webcam=N", "--play_video=Y", "--video_path=test3.mp4"])
    while True:
        try:
            with sr.Microphone() as source:
                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    print("before listen")
                    audio = recognizer.listen(source)
                    my_text = recognizer.recognize_google(audio)
                    if len(my_text) > 0:
                        print("** text: ",my_text)
                        brain.brain(my_text,  model, classes, colors, output_layers)
        except Exception as e:
            print("Error: ",e)

    '''while 1:
        # get the trigger using text to speech
        try:
            if video_getter.stopped or video_shower.stopped:
                video_shower.stop()
                video_getter.stop()
                break
            frame = video_getter.frame
            video_shower.frame = frame
            with sr.Microphone() as source:
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source)
                my_text = recognizer.recognize_google(audio)
                if len(my_text) > 0:
                    brain.brain(my_text)
'''
main()
