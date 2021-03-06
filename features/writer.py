from abc import ABCMeta, abstractmethod


class Writer(metaclass=ABCMeta):
    def __init__(self):
        self.data = None

    @abstractmethod
    def write(self, wav_path, text_path, grid_path, file):
        raise NotImplementedError()
