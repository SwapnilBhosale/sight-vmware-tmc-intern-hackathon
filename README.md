
# sight-vmware-tmc-intern-hackathon

Hackathon project part of VMWare intern 2020

## Contents

[***Introduction***](https://github.com/SwapnilBhosale/sight-vmware-tmc-intern-hackathon#Introduction)

[***Prerequisites***](https://github.com/SwapnilBhosale/sight-vmware-tmc-intern-hackathon#Prerequisites)

[***Instructions***](https://github.com/SwapnilBhosale/sight-vmware-tmc-intern-hackathon#Instructions)

[***Results And Demo***](https://github.com/SwapnilBhosale/sight-vmware-tmc-intern-hackathon#Results)

[***Future Work***](https://github.com/SwapnilBhosale/sight-vmware-tmc-intern-hackathon#FutureWork)


## Introduction

This is a project aims in helping visually impared users **seeing** the world.

Key features include:

- ***Object Detection and Recognition***: the integrated speaker can speak what's in front of the camera via voice commands.

- ***Image Capture and Captioning***: capture the image on camera with voice command trigger, and generate a descriptive sentence as voice output. 

- ***Text Reader***: detect text present in front of camera and enable speaker to read the text for users.

## Prerequisites 

Run project with Webcam

```
1) brew install portaudio

2) pip3 install -r requirements.txt

3) python3 main.py

```


Run project with Video

```
1) brew install portaudio

2) pip3 install -r requirements.txt

3) python3 main.py --webcam=N

```

### Speech to Text

Run following commands to install dependencies

```
1) brew install portaudio

2) pip3 install -r requirements.txt

3) python3 speech_to_text.py

```


### Image detenction

Run following commands to install dependencies

```
1) wget https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5

2) python3 image_detection_yolo.py

3) brew install tesseract

```

## Instruction

- ***Object Detection and Recognition***: Run `main.py` and wait for modules to load. Provide the flag `--webcam N` if you wish to see the demo with a preloaded video for object detection. Once loaded, it will prompt user for voice input. Ask with microphone `What do you see` or `what is this`, then wait for speaker module to generate the voice and you should be able to hear the output within a few seconds.

## Results And Demo

![Object Detection](https://github.com/SwapnilBhosale/sight-vmware-tmc-intern-hackathon/blob/master/demo_data/object_detection.png?raw=true)
