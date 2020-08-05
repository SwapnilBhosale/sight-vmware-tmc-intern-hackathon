import re

import cv2
import numpy as np
import pytesseract


def get_string_from_img(img_path):
    res = None
    img = cv2.imread(img_path)
    img = remove_noise(img)
    extracted_text = get_string(img)
    print("extracted_text: ",extracted_text)
    if len(extracted_text) > 0:
        res =  str(extracted_text)
    print("*** read the text: ",res)
    return res

def get_string(img):
    return pytesseract.image_to_string(img)


def remove_noise(img):
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    
    return img      



if __name__ == "__main__":
    print(get_string_from_img("current.png"))
