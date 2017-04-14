from abc import ABCMeta, abstractmethod


class Splitter(metaclass=ABCMeta):
    def __init__(self, num_of_out_features):
        self.num_of_out_features = num_of_out_features

    @abstractmethod
    def split(self, data):
        raise NotImplementedError()
