import numpy as np
import sys
from DataProcessor import DataProc
from Model import ModelTrainer


class main:
    def __init__(self):
        # CNN Training parameters
        class Settings:
            samples = 0
            indexes = []
            img_size = [60, 50, 50]
            img_data = ['./Actions/Hello/', './Actions/Dog/', './Actions/Eat/']
            batch_size = 100
            class_cnt = len(img_data)
            epoch_cnt = 100
            filters = [32, 32]
            pool_size = [5, 5, 5]
            kernal_shape = [5, 2, 2]

        data_process = DataProc(Settings)
        (X_tr, indexes) = data_process.load_folders(Settings.img_data)
        Settings.indexes = indexes
        X_train_arr = np.array(X_tr)
        Settings.samples = len(X_train_arr)
        X_tests = [[], [], []]

        test_vid_dir = './Actions/'
        test_vids = ['Test_Dog.avi', 'Test_Hello.avi', "Test_Eat.avi"];
        for i in range(len(X_tests)):
            data_process.read_dataset([test_vids[i]], test_vid_dir, X_tests[i]);

        img_rows, img_cols, img_depth = Settings.img_size[2], Settings.img_size[1], Settings.img_size[0]

        test_sets = []

        for i in X_tests:
            x_test_array = np.array(i)
            test_cnt = len(x_test_array)
            test_sets.append(np.zeros((test_cnt, 1, img_depth, img_rows, img_cols)))

        model_factory = ModelTrainer()

        model = model_factory.createmodel(Settings)

        model_factory.train(model, X_train_arr, Settings)

        classes = ["Hello", "Dog", "Eat"]
        for vid in range(len(test_sets)):
            print("INPUT:", test_vids[vid])
            y_prob = model.predict(test_sets[vid], batch_size=Settings.batch_size)
            print(y_prob)
            y_classes = y_prob.argmax(axis=-1)
            print("OUTPUT:", classes[int(y_classes)], y_classes)


main()
