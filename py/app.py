from keras.preprocessing.image import ImageDataGenerator
import keras.models
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution3D, MaxPooling3D

from keras.optimizers import SGD, RMSprop
from keras.utils import np_utils, generic_utils

import tensorflow as tf
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import ffmpeg

from sklearn.model_selection  import train_test_split


# image specification
img_rows,img_cols,img_depth=480,640,42


# Training data

X_tr=[]           # variable to store entire dataset

#Reading boxing action class
path = 'C:\\Users\\kolcr\\PycharmProjects\\3DCnn\\clips\\'
listing = os.listdir(path)

for vid in listing:
    vid = path+vid
    images = []
    frames = []
    print(vid)
    probe = ffmpeg.probe(vid)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])

    out, err = (
        ffmpeg
            .input(vid)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True)
    )
    video = (
        np
            .frombuffer(out, np.uint8)
            .reshape([-1, height, width])
    )

    ipt=np.rollaxis(np.rollaxis(video,2,0),2,0)

    X_tr.append(ipt)


X_tr_array = np.array(X_tr)  # convert the frames read into array

num_samples = len(X_tr_array)
print("Num Samples: " + str(num_samples))

# Assign Label to each class

label = np.ones((num_samples,), dtype=int)
label[0:100] = 0
label[100:199] = 1
label[199:299] = 2
label[299:399] = 3
label[399:499] = 4
label[499:] = 5

train_data = [X_tr_array, label]

(X_train, y_train) = (train_data[0], train_data[1])
print('X_Train shape:', X_train.shape)

train_set = np.zeros((num_samples, 1, img_rows, img_cols, img_depth))

for h in range(num_samples):
    train_set[h][0][:][:][:] = X_train[h, :, :, :]

patch_size = 42 # img_depth or number of frames used for each video

print(train_set.shape, 'train samples')

# CNN Training parameters

batch_size = 2
nb_classes = 6
nb_epoch = 50

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

model = keras.models.Sequential()
#(nb_filters[0], nb_depth=nb_conv[0], nb_row=nb_conv[0], nb_col=nb_conv[0],
#                       , activation='relu'))

model.add(keras.layers.Conv3D(nb_filters[0], (3, 3, 3), input_shape=(img_rows, img_cols, patch_size, 1)))

model.add(keras.layers.MaxPooling3D(pool_size=(nb_pool[0], nb_pool[0], nb_pool[0])))

model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Flatten())

model.add(keras.layers.Dense(128, kernel_initializer=keras.initializers.normal, activation='relu'))

model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(nb_classes, kernel_initializer=keras.initializers.normal))

model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='RMSprop')

# Split the data

X_train_new, X_val_new, y_train_new, y_val_new = train_test_split(train_set, Y_train, test_size=0.2, random_state=4)

# Train the model

hist = model.fit(X_train_new, y_train_new, validation_data=(X_val_new, y_val_new),
                 batch_size=batch_size, nb_epoch=nb_epoch, show_accuracy=True, shuffle=True)

# hist = model.fit(train_set, Y_train, batch_size=batch_size,
#         nb_epoch=nb_epoch,validation_split=0.2, show_accuracy=True,
#           shuffle=True)


# Evaluate the model
score = model.evaluate(X_val_new, y_val_new, batch_size=batch_size, show_accuracy=True)
print('Test score:', score[0])
print('Test accuracy:', score[1])

# Plot the results
train_loss = hist.history['loss']
val_loss = hist.history['val_loss']
train_acc = hist.history['acc']
val_acc = hist.history['val_acc']
xc = range(100)

plt.figure(1, figsize=(7, 5))
plt.plot(xc, train_loss)
plt.plot(xc, val_loss)
plt.xlabel('num of Epochs')
plt.ylabel('loss')
plt.title('train_loss vs val_loss')
plt.grid(True)
plt.legend(['train', 'val'])
print
plt.style.available  # use bmh, classic,ggplot for big pictures
plt.style.use(['classic'])

plt.figure(2, figsize=(7, 5))
plt.plot(xc, train_acc)
plt.plot(xc, val_acc)
plt.xlabel('num of Epochs')
plt.ylabel('accuracy')
plt.title('train_acc vs val_acc')
plt.grid(True)
plt.legend(['train', 'val'], loc=4)
# print plt.style.available # use bmh, classic,ggplot for big pictures
plt.style.use(['classic'])