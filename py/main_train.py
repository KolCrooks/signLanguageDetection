import numpy as np
import os
import matplotlib.pyplot as plt
from DataProcessor import DataProc
from Model import ModelTrainer
import Settings


class Main:
    def __init__(self):
        # CNN Training parameters

        data_process = DataProc(Settings)
        (X_tr, indexes) = data_process.load_folders(Settings.img_data)
        Settings.indexes = indexes
        X_train_arr = np.array(X_tr)
        Settings.samples = len(X_train_arr)

        test_vid_dir = ['./Actions/tests/']
        test_vids = os.listdir(test_vid_dir[0])
        (X_tests, _) = data_process.load_folders(test_vid_dir)
        # for i in range(len(X_tests)):
        #     data_process.read_dataset([test_vids[i]], test_vid_dir, X_tests[i]);

        test_sets = np.array(X_tests[0])


        model_factory = ModelTrainer()

        model = model_factory.createmodel(Settings)

        hist = model_factory.train(model, X_train_arr, Settings)
        model_factory.save_model(model, "./model/")
        # Plot the results
        train_loss = hist.history['loss']
        val_loss = hist.history['val_loss']
        train_acc = hist.history['acc']
        val_acc = hist.history['val_acc']
        xc = range(Settings.epoch_cnt)

        plt.figure(1, figsize=(7, 5))
        plt.plot(xc, train_loss)
        plt.plot(xc, val_loss)
        plt.xlabel('num of Epochs')
        plt.ylabel('loss')
        plt.title('train_loss vs val_loss')
        plt.grid(True)
        plt.legend(['train', 'val'])

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

        classes = ["Hello", "Dog", "Eat"]

        for vid in range(len(test_sets)):
            print("INPUT:", test_vids[vid])
            in_vid = np.zeros((1, 1, Settings.img_size[0], Settings.img_size[1], Settings.img_size[2]))
            in_vid[0][0][:][:][:] = test_sets[vid, :, :, :]

            y_prob = model.predict(in_vid, batch_size=1)
            print(y_prob)
            y_classes = y_prob.argmax(axis=-1)
            print("OUTPUT:", classes[int(y_classes)], y_classes)
            print("")

        plt.show()

Main()
