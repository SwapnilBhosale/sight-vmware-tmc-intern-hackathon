import cv2
from imageai import Detection


def create_and_load_yolo(model_path):
    yolo = Detection.ObjectDetection()
    yolo.setModelTypeAsYOLOv3()
    yolo.setModelPath(model_path)
    yolo.loadModel()
    return yolo


def open_and_set_webcam():

    cam = cv2.VideoCapture(0) #0=front-cam, 1=back-cam
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1300)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1500)
    return cam


def main():
    yolo = create_and_load_yolo("yolo.h5")
    cam = open_and_set_webcam()

    while True:
        ## read frames
        ret, img = cam.read()
        ## predict yolo
        img, preds = yolo.detectCustomObjectsFromImage(input_image=img, 
                        custom_objects=None, input_type="array",
                        output_type="array",
                        minimum_percentage_probability=70,
                        display_percentage_probability=False,
                        display_object_name=True)
        ## display predictions
        print("Predicted labels: ",preds)
        cv2.imshow("", img)
        ## press q or Esc to quit    
        if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27):
            break
    ## close camera
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
