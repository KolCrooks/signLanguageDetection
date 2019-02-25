import cv2
import glob
import numpy as np
import os
import skimage

# Image Specification (rows and column are the size, depth is the number of frames that will be stacked upon each other)
img_rows, img_cols, img_depth = 28, 28, 15

# Takes in a video capture through folder
cap = cv2.VideoCapture('C:/Users/Sean McHale/Pictures/Camera Roll/dance.webm')
print(cap.isOpened())
print("\t Number of Frames: ", cap.get(7))
print("\t Width: ", cap.get(3))
print("\t Height: ", cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output_video.avi", fourcc, 20.0, (640, 360))
print(out.isOpened())


while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (img_rows, img_cols), interpolation=cv2.INTER_AREA)
    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

cv2.waitKey(0)
