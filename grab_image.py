import cv2

#Thread for capturing image from video feed
def grab_image(memory={}):

    video_capture = cv2.VideoCapture(0)

    while memory.get("running"):
        success, image = video_capture.read()
        if success:
            memory["raw_image"] = image  #Raw image is to be used by processing thread
    video_capture.release()
