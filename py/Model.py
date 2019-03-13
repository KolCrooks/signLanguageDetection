import keras
from keras import backend as K
from keras.layers.convolutional import Convolution3D, MaxPooling3D
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import SGD
from keras.models import Sequential
from keras.callbacks import CSVLogger
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
import numpy as np


class ModelTrainer:

    def createmodel(self, settings):

        filters = settings.filters
        kernal_shape = settings.kernal_shape
        img_shape = [1] + settings.img_size
        pool_size = settings.pool_size
        class_cnt = settings.class_cnt
        # Define model
        model = Sequential()
        #(1, img_depth, img_cols, img_rows)
        model.add(Convolution3D(filters[0], kernel_size=kernal_shape, input_shape=img_shape,
                                kernel_constraint=keras.constraints.max_norm(),
                                activation='relu'))

        model.add(MaxPooling3D(pool_size=pool_size))

        model.add(Dropout(0.5))

        model.add(Flatten())

        model.add(Dense(128, activation='relu'))

        model.add(Dropout(0.5))

        model.add(Dense(class_cnt, activation='relu'))

        model.add(Activation('softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='RMSprop')

        return model;

    def train(self, model, x_tr_array, train_settings):
        batch_size = train_settings.batch_size
        epoch_cnt = train_settings.epoch_cnt
        indexes = train_settings.indexes
        temp = []
        for ar in x_tr_array:
            for t in ar:
                temp.append(t)

        x_tr_array = np.array(temp)
        num_samples = len(x_tr_array)

        # Assign Label to each class
        label = np.ones((num_samples,), dtype=int)
        label[0:indexes[0]] = 0  # Hello
        label[indexes[0]:sum(indexes[0:1])] = 1  # Dog
        label[sum(indexes[0:1]):sum(indexes[0:2])] = 2  # Eat
        # label[sum(indexes[0:2]):sum(indexes[0:3])] = 3 # Hands up Down
        # label[sum(indexes[0:3]):] = 4  #Open Close

        train_data = [x_tr_array, label]

        (X_train, y_train) = (train_data[0], train_data[1])
        print('X_Train shape:', X_train.shape)

        train_set = np.zeros((num_samples, 1, train_settings.img_size[0], train_settings.img_size[1],
                              train_settings.img_size[2]))
        for h in range(num_samples):
            train_set[h][0][:][:][:] = X_train[h, :, :, :]

        Y_train = np_utils.to_categorical(y_train, train_settings.class_cnt)
        # Pre-processing
        train_set = train_set.astype('float32')

        train_set -= np.mean(train_set)

        train_set /= np.max(train_set)

        # Split the data

        X_train_new, X_val_new, y_train_new, y_val_new = train_test_split(train_set, Y_train, test_size=0.2, random_state=0)

        # Train the model
        opt = SGD(lr=0.001)

        model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['acc'])
        csv_logger = CSVLogger('log.csv', append=True, separator=';')

        hist = model.fit(X_train_new, y_train_new, validation_data=(X_val_new, y_val_new),
                         batch_size=batch_size, epochs=epoch_cnt, shuffle=True, callbacks=[csv_logger])

        # Test Mode
        score = model.evaluate(X_val_new, y_val_new, batch_size=batch_size)
        print(score)

        return hist

    def __init__(self):
        K.set_image_dim_ordering('th')
