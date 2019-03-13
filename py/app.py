import numpy as np
import sys
from DataProcessor import DataProc
from Model import ModelTrainer
from PIL import Image

class main:
    def __init__(self):
        # CNN Training parameters
        class Settings:
            samples = 0
            indexes = []
            img_size = [60, 50, 50]
            img_data = ['./Actions/Hello/', './Actions/Dog/', './Actions/Eat/']
            batch_size = 2
            class_cnt = len(img_data)
            epoch_cnt = 10
            filters = [32, 16]
            pool_size = [3, 3, 3]
            kernal_shape = [2, 2, 2]

        data_process = DataProc(Settings)
        (X_tr, indexes) = data_process.load_folders(Settings.img_data)
        Settings.indexes = indexes
        X_train_arr = np.array(X_tr)
        Settings.samples = len(X_train_arr)

        test_vid_dir = ['./Actions/tests/']
        test_vids = ['Test_Dog.avi', 'Test_Hello.avi', "Test_Eat.avi"];
        (X_tests, _) = data_process.load_folders(test_vid_dir)
        # for i in range(len(X_tests)):
        #     data_process.read_dataset([test_vids[i]], test_vid_dir, X_tests[i]);

        test_sets = np.array(X_tests[0])


        model_factory = ModelTrainer()

        model = model_factory.createmodel(Settings)

        model_factory.train(model, X_train_arr, Settings)

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


main()
