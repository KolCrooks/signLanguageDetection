from DataProcessor import DataProc
from Model import ModelTrainer
import numpy as np
import Settings


class Main:
    classes = ["Hello", "Dog", "Eat"]

    def __init__(self):
        # Load Model
        model_load = ModelTrainer()
        self.model = model_load.load_from_json("./model")
        self.data_process = DataProc(Settings)

        while True:
            self.listen()

    def listen(self):



Main()