import numpy as np
from detect_color import detect_color
import cv2
from motor_control import TARGET_X, TARGET_Y, THRESHOLD

TARGET_START = (int(TARGET_X - THRESHOLD // 2), int(TARGET_Y - THRESHOLD // 2))
TARGET_END = (int(TARGET_X + THRESHOLD // 2), int(TARGET_Y + THRESHOLD // 2))

#Image processing thread
def process_image(memory={}):
    while memory.get("running"):
        image = memory.get("raw_image") #get raw image from grab image thread
        if image is not None:
            image = image.copy()
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hue, saturation, value = cv2.split(hsv)
            success, threshold = cv2.threshold(saturation, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            if success:
                median_blur = cv2.medianBlur(threshold, 15)
                contours, hierarchy = cv2.findContours(median_blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                final = np.zeros(image.shape,np.uint8) #Image without shapes
                mask = np.zeros(median_blur.shape,np.uint8) #Mask for shape contours

                for (index, contour) in enumerate(contours):
                        mask[...]=0
                        cv2.drawContours(mask,contours,index,255,-1)
                        cv2.drawContours(final,contours,index,cv2.mean(image,mask),-1)

                        B,G,R,_ = cv2.mean(image,mask)
                        display_text = detect_color(R,G,B)

                        moments = cv2.moments(contour)

                        if moments["m00"]:
                            cX = int(moments["m10"] / moments["m00"])
                            cY = int(moments["m01"] / moments["m00"])
                        else:
                            cX = 0
                            cY = 0

                        #Target color updated from command lines thread
                        if display_text == memory["target"]:
                            memory["centroid"] = {
                                "cX": cX,
                                "cY": cY,
                            }

                        #Place a dot on colored centroids
                        cv2.circle(final, (cX, cY), 5, (255, 255, 255), -1)
                        cv2.putText(final, display_text, (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                memory["image"] = final #Image to be displayed by display image thread
