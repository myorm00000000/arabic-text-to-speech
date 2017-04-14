from abc import ABCMeta, abstractmethod
import numpy as np


class Loader(metaclass=ABCMeta):
    def __init__(self):
        self.data = None

    @abstractmethod
    def load(self, wav_path, text_path, grid_path, f):
        raise NotImplementedError()

    def get_as_array(self):
        return self.data

    def get_as_numpy_array(self):
        return np.array(self.data)
