from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution3D, MaxPooling3D

from keras.optimizers import SGD, RMSprop
from keras.utils import np_utils, generic_utils

# import theano
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn import preprocessing


# Image Specification (rows and column are the size, depth is the number of frames that will be stacked upon each other)
img_rows, img_cols, img_depth = 28, 28, 15

# Video that you want to test?
# Takes in a video capture through folder

# cap = cv2.VideoCapture('C:/Users/Sean McHale/Documents/ASL Recognition/signLanguageDetection/clips/hands.webm')
# print(cap.isOpened())


# Training Data

# variable to store entire data set
X_tr = []

listing = os.listdir('C:/Users/Sean McHale/Documents/DataSets/Actions/handMoving.mp4')

for vid in listing:
    vid = 'C:/Users/Sean McHale/Documents/DataSets/Actions/handMoving.mp4' + vid
    frames = []
    cap = cv2.VideoCapture(vid)
    fps = cap.get(5)
    print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))

    for k in range(15):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (img_rows, img_cols), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray)

    plt.imshow(gray, cmap=plt.get_cmap('gray'))
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()
    cv2.imshow('frame', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

input = np.array(frames)

print(input.shape)
ipt = np.rollaxis(np.rollaxis(input, 2, 0), 2, 0)
print(ipt.shape)

X_tr.append(ipt)

success, image = cap.read()

count = 1

# Saves each frame
while success:
    cv2.imwrite("C:/Users/Sean McHale/Documents/DataSets/Frames/frame%d.jpg" % count, image)  # save frame as JPEG file
    success, image = cap.read()
    print('Read a new frame: ', success)
    count += 1

frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

images = []
files = glob.glob("C:/Users/Sean McHale/Documents/DataSets/Frames/*.jpg")
for myFile in files:
    print(myFile)
    image = cv2.imread(myFile)
    images.append(image)

print('Images shape:', np.array(images).shape)
print(images[0])


# print(frameCount)

