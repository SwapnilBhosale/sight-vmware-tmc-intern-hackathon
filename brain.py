

from random import randrange

import cv2
import image_detection_yolo as yolo
import text_to_speech
from PIL import Image, ImageDraw, ImageFont
from text_caption import getImageCaption
from text_read import get_string_from_img

sentences = [
    "There is a {} in front of you",
    "I see {}"
]

def brain(data, model, classes, colors, output_layers):
    image = cv2.imread('current.png')
   
    if data and ("hi" in data or "what is this" in data or "what is" in data or "do you see" in data):
        text_to_speech.SpeakText("Let me see")
        print("before imge_process")
        statement = image_process(image, model, classes, colors, output_layers)
        text_to_speech.SpeakText(statement)
    elif data and ("describe" in data or "descibe surrounding" in data):
        #Here let's integrate the desctibe call
        res = getImageCaption("./current.png")
        if not res:
            text_to_speech.SpeakText("Sorry there is no text to read")
        else:
            text_to_speech.SpeakText(res)
    elif data and ("read it" in data or "please read" in data):
        res = get_string_from_img("./current.png")
        if not res:
            text_to_speech.SpeakText("Sorry there is no text to read")
        else:
            text_to_speech.SpeakText(res)
    else:
        text_to_speech.SpeakText("Sorry! I don't understand")

def image_process(frame, model, classes, colors, output_layers):
    height, width, channels = frame.shape
    blob, outputs = yolo.detect_objects(frame, model, output_layers)
    boxes, confs, class_ids = yolo.get_box_dimensions(outputs, height, width)
    print("*** confs:{} {} ".format(max(confs), classes[class_ids[confs.index(max(confs))]]))
    print("***8 class_ids:  ",class_ids)
    #print_labels(classes,class_ids)

    i = randrange(0, len(sentences))
    return sentences[i].format(classes[class_ids[confs.index(max(confs))]])
