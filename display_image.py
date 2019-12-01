import cv2


#Thread for displaying image
def display_image(memory={}):
    while memory.get("running"):
        image = memory.get("image") #Display processed image from process image thread
        if image is not None:
            cv2.imshow("Peidi and Sebastien Image", image)
        if cv2.waitKey(25) == ord("q"):
            memory["running"] = False
    cv2.destroyAllWindows()
    
