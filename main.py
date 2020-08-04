
import time

import brain
import speak
import speech_to_text


def main():
         
    time.sleep(2)
    while 1:
        #get the trigger using text to speech
        data = "you see" 
        brain.brain(data)

    
if __name__ == '__main__':
    main()
