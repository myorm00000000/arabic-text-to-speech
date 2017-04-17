import numpy as np
from signal_processing.window_type import WindowType


class SignalSmoother:
    def __init__(self, signal):
        self.signal = signal

    def smooth(self, window_type=WindowType.hamming, length=40):
        norm = None
        if window_type == WindowType.hanning:
            norm = np.hanning(length) / sum(np.hanning(length))
            pass
        elif window_type == WindowType.hamming:
            norm = np.hamming(length) / sum(np.hamming(length))
            pass
        else:
            pass
        return np.convolve(self.signal, norm)
