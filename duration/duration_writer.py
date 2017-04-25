import math
import os

import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf
from textgrid import TextGrid

import pyworld as pw
from features.writer import Writer
from phoneme.phonetise import phonetise
from training.feature_extractor import FeatureExtractor
from training.feature_reader import FeatureReader


class DurationWriter(Writer):
    def write(self, wav_path, text_path, grid_path, file):
        grid = TextGrid("test")
        grid.read(grid_path)
        intervals = grid.getList("phones")[0].intervals
        with open(text_path, 'r') as ff:
            (_, _, _, d) = phonetise(ff.read(), arabic=False)
            phonemes = FeatureExtractor(d).get_features()
        for interval, phoneme in zip(intervals, phonemes):
            minTime = interval.minTime
            maxTime = interval.maxTime
            features = phoneme + [maxTime - minTime]
            file.write(",".join(list(map(str, features))) + "\n")
