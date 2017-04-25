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


class FeatureWriter(Writer):
    def write(self, wav_path, text_path, grid_path, file):
        grid = TextGrid("test")
        grid.read(grid_path)
        intervals = grid.getList("phones")[0].intervals
        intervals = [i for i in intervals if i.text != "sil"]
        with open(text_path, 'r') as ff:
            (_, _, _, d) = phonetise(ff.read(), arabic=False)
            phonemes = FeatureExtractor(d).get_features()
        temp_path = "temp.wav"
        for interval, phoneme in zip(intervals, phonemes):
            minTime = interval.minTime
            maxTime = interval.maxTime
            FeatureWriter.cut(wav_path, minTime, maxTime, temp_path)
            x, fs = sf.read(temp_path)
            f0, sp, ap = pw.wav2world(x, fs, frame_period=FeatureReader.frame_length)
            num_of_frames = int(math.ceil((maxTime - minTime) / float(FeatureReader.frame_length)))
            for frame, f, s, a in zip(range(1, num_of_frames + 1), f0, sp, ap):
                features = [frame] + phoneme
                outpu = [f] + s + a
                features = np.concatenate((features, outpu))
                file.write(",".join(list(map(str, features))) + "\n")
            os.system("rm {}".format(temp_path))

    @staticmethod
    def cut(wav_path, minTime, maxTime, temp_path):
        command = "sox {} {} trim {} ={}".format(wav_path, temp_path, minTime, maxTime)
        os.system(command)
        return wav.read(temp_path)
