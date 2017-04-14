import random

import numpy as np
from splitter import Splitter


class StaticSplitter(Splitter):
    def __init__(self, num_of_out_features, ratio=0.7):
        super().__init__(num_of_out_features)
        self.ratio = ratio

    def split(self, data):
        data = random.sample(data, len(data))
        a = int(len(data) * self.ratio)
        b = len(data[0]) - self.num_of_out_features
        t1, t2 = data[:a], data[a:]
        x_train, y_train, x_test, y_test = [], [], [], []
        for row in t1:
            print(len(row[:b]))
            x_train.append(row[:b])
            y_train.append(row[b:])
        for row in t2:
            x_test.append(row[:b])
            y_test.append(row[b:])
        return (np.matrix(x_train), np.matrix(y_train)), (np.matrix(x_test), np.matrix(y_test))
