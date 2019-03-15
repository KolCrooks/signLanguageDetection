from DataProcessor import DataProc
from Model import ModelTrainer
import numpy as np
import os
import Settings


class Main:
    model_load = ModelTrainer()

    model = model_load.load_from_json("./model")
    data_process = DataProc(Settings)
    test_vid_dir = ['./Actions/tests/']
    test_vids = os.listdir(test_vid_dir[0])
    (X_tests, _) = data_process.load_folders(test_vid_dir)
    # for i in range(len(X_tests)):
    #     data_process.read_dataset([test_vids[i]], test_vid_dir, X_tests[i]);

    test_sets = np.array(X_tests[0])

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


Main()
