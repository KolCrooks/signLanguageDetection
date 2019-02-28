from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution3D, MaxPooling3D

from keras.optimizers import SGD, RMSprop
from keras.utils import np_utils, generic_utils


import os
import sys

import numpy as np
import cv2

from sklearn.model_selection import train_test_split

from keras import backend as K

CURSOR_UP_ONE = '\033[F'
ERASE_LINE = '\033[K'
loading = ["|", "/","-","\\"]
img_rows, img_cols, img_depth = 75, 75, 60

def replace_line(n_line):
    sys.stdout.write("\r" + n_line)
    sys.stdout.flush()

def read_dataset(videos, directory, input_list):
    vid_cnt = 0
    print("Loading " + directory)
    for vid in videos:
        vid = directory + vid
        frames = []
        cap = cv2.VideoCapture(vid)
        while True:
            ret, frame = cap.read()
            if frame is None:
                break
            frame = cv2.resize(frame, (img_rows, img_cols), interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray)

        vid_cnt += 1
        replace_line("Loading Dataset (" + str(vid_cnt) + "/" + str(len(videos)) + ") " + str(len(frames)))

        cnt = 0
        cnt2 = 0
        if len(frames) > img_depth:
            while len(frames) > img_depth:
                del frames[cnt]
                cnt += 1
                cnt2 += 1
                cnt %= len(frames)
                replace_line("Loading Dataset (" + str(vid_cnt) + "/" + str(len(videos)) + ") " + loading[cnt2%len(loading)])
        else:
            while len(frames) < img_depth:
                frames.insert(cnt, frames[cnt])
                cnt += 2
                cnt2 += 1
                cnt %= len(frames)
                replace_line("Loading Dataset (" + str(vid_cnt) + "/" + str(len(videos)) + ") " + loading[cnt2%len(loading)])

    replace_line("Loading Dataset (" + str(len(videos)) + "/" + str(len(videos)) + ")\t Done.")
    cap.release()
    cv2.destroyAllWindows()
    input = np.array(frames)
    ipt = np.rollaxis(np.rollaxis(input, 2, 0), 2, 0)  # to make data in image row, image column, image depth
    input_list.append(ipt)


K.set_image_dim_ordering('th')



# print(frameCount)
# Test Video
X_test = []
test_vid_dir = './Actions/'
test_vid = 'Test_Eat.avi';
read_dataset([test_vid], test_vid_dir, X_test);
print("\n")
X_test_array = np.array(X_test)
num_samples2 = len(X_test_array)
test_set = np.zeros((num_samples2, 1, img_rows, img_cols, img_depth))


# Where all data sets will be stored
X_tr = []
data = ['./Actions/Hello/','./Actions/Dog/','./Actions/Eat/']

# handMoving Data set
indexes = []
for p in data:
    listing = os.listdir(p)
    indexes.append(len(listing))
    read_dataset(listing, p, X_tr);
    print("\n")



X_tr_array = np.array(X_tr)  # convert the frames read into array

num_samples = len(X_tr_array)

# Assign Label to each class
label = np.ones((num_samples,), dtype=int)
label[0:indexes[0]] = 0                         #Hello
label[indexes[0]:sum(indexes[0:1])] = 1         #Dog
label[sum(indexes[0:1]):sum(indexes[0:2])] = 2  #Eat
# label[sum(indexes[0:2]):sum(indexes[0:3])] = 3 # Hands up Down
# label[sum(indexes[0:3]):] = 4  #Open Close

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

X_train_new, X_val_new, y_train_new, y_val_new = train_test_split(train_set, Y_train, test_size=0.5, random_state=5)

# Train the model
opt = SGD(lr=0.001)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['acc'])
hist = model.fit(X_train_new, y_train_new, validation_data=(X_val_new, y_val_new),
                 batch_size=batch_size, epochs=nb_epoch, shuffle=True)

# Test Mode
score = model.evaluate(X_val_new, y_val_new, batch_size=batch_size)
print(score)

y_prob = model.predict(test_set, batch_size=2)
print(y_prob)
y_classes = y_prob.argmax(axis=-1)
classes = ["Hello","Dog","Eat"]
print("INPUT:", test_vid)
print("OUTPUT:", classes[int(y_classes)], y_classes)

