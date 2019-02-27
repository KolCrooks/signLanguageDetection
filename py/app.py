from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution3D, MaxPooling3D

from keras.optimizers import SGD, RMSprop
from keras.utils import np_utils, generic_utils


import os

import numpy as np
import cv2

from sklearn.model_selection import train_test_split

from keras import backend as K


def readdataset(videos,dir,retList):

    for vid in videos:
        vid = dir + vid
        frames = []
        cap = cv2.VideoCapture(vid)
        while True:
            ret, frame = cap.read()
            if frame is None:
                break;
            frame = cv2.resize(frame, (img_rows, img_cols), interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray)
        print("frame count: " + str(len(frames)))
        cnt = 0
        if len(frames) > img_depth:
            while len(frames) > img_depth:
                del frames[cnt]
                cnt += 1
                cnt %= len(frames)
        else:
            while len(frames) < img_depth:
                print(cnt)
                print(len(frames))
                frames.insert(cnt,frames[cnt])
                cnt += 2
                cnt %= len(frames)


    cap.release()
    cv2.destroyAllWindows()
    input = np.array(frames)
    print(input.shape)
    ipt = np.rollaxis(np.rollaxis(input, 2, 0), 2, 0)  # to make data in image row, image column, image depth
    print(ipt.shape)
    retList.append(ipt)


K.set_image_dim_ordering('th')


img_rows, img_cols, img_depth = 56, 56, 60

# print(frameCount)
# Test Video
X_test = []
vid = './Actions/'
readdataset(['testAVI.avi'], vid, X_test);

X_test_array = np.array(X_test)
num_samples2 = len(X_test_array)
test_set = np.zeros((num_samples2, 1, img_rows, img_cols, img_depth))


# Where all data sets will be stored
X_tr = []

# handMoving Data set
pathHM = './Actions/handMoving/'
listingHM = os.listdir(pathHM)
readdataset(listingHM, pathHM, X_tr);

# hands collide data set
pathHC = './Actions/handsCollide/'
listingHC = os.listdir(pathHC)
readdataset(listingHC, pathHC, X_tr);

# HandsUpAway data set
pathHUA = './Actions/handsUpAway/'
listingHUA = os.listdir(pathHUA)
readdataset(listingHUA, pathHUA, X_tr);

# handsUpDown data set
pathHUP = './Actions/handsUpDown/'
listingHUP = os.listdir(pathHUP)
readdataset(listingHUP, pathHUP, X_tr);

# open close data set
pathOC = './Actions/openClose/'
listingOC = os.listdir(pathOC)
readdataset(listingOC, pathOC, X_tr);


X_tr_array = np.array(X_tr)  # convert the frames read into array

num_samples = len(X_tr_array)
print(num_samples)

# Assign Label to each class
label = np.ones((num_samples,), dtype=int)
label[0:len(listingHM)] = 0 #Hand Moving
label[len(listingHM):len(listingHM)+len(listingHC)] = 1 #Hands colliding
label[len(listingHM)+len(listingHC):len(listingHM)+len(listingHC)+len(listingHUA)] = 2 # Hands up away
label[len(listingHM)+len(listingHC)+len(listingHUA):len(listingHM)+len(listingHC)+len(listingHUA)+len(listingHUP)] = 3 # Hands up Down
label[len(listingHM)+len(listingHC)+len(listingHUA)+len(listingHUP):] = 4  #Open Close

train_data = [X_tr_array, label]

(X_train, y_train) = (train_data[0], train_data[1])
print('X_Train shape:', X_train.shape)

train_set = np.zeros((num_samples, 1, img_rows, img_cols, img_depth))
for h in range(num_samples):
    train_set[h][0][:][:][:] = X_train[h, :, :, :]

patch_size = 90  # img_depth or number of frames used for each video

print(train_set.shape, 'train samples')

# CNN Training parameters
batch_size = 100
nb_classes = 5
nb_epoch = 100

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)


# number of convolutional filters to use at each layer
nb_filters = [32, 32]

# level of pooling to perform at each layer (POOL x POOL)
nb_pool = [3, 3]

# level of convolution to perform at each layer (CONV x CONV)
nb_conv = [5, 5]

# Pre-processing

train_set = train_set.astype('float32')

train_set -= np.mean(train_set)

train_set /= np.max(train_set)

# Define model
model = Sequential()

model.add(Convolution3D(nb_filters[0], kernel_dim1=nb_conv[0], kernel_dim2=nb_conv[0], kernel_dim3=nb_conv[0],
                        input_shape=(1, img_rows, img_cols, img_depth), activation='relu'))

model.add(MaxPooling3D(pool_size=(nb_pool[0], nb_pool[0], nb_pool[0])))

model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(128, activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(nb_classes, activation='relu'))

model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='RMSprop')

# Split the data

X_train_new, X_val_new, y_train_new, y_val_new = train_test_split(train_set, Y_train, test_size=0.2, random_state=2)

# Train the model
opt = SGD(lr=0.001)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['acc'])
hist = model.fit(X_train_new, y_train_new, validation_data=(X_val_new, y_val_new),
                 batch_size=batch_size, epochs=nb_epoch, shuffle=True)

# Test Mode
score = model.evaluate(X_val_new, y_val_new, batch_size=batch_size)
print(score)

y_prob = model.predict(test_set, batch_size=2)
y_classes = y_prob.argmax(axis=-1)

print(y_classes)

