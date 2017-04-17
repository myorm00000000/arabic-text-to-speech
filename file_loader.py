import os

import numpy as np
import scipy.io.wavfile as wav
import soundfile as sf
import pyworld as pw
from textgrid import TextGrid
from training.feature_reader import FeatureReader
import math

from loader import Loader
from phoneme.phonetise import phonetise
from training.feature_extractor import FeatureExtractor


class FileLoader(Loader):
    def load(self, wav_path, text_path, grid_path, file):
        grid = TextGrid("test")
        grid.read(grid_path)
        intervals = grid.getList("phones")[0].intervals
        with open(text_path, 'r') as ff:
            (_, _, _, d) = phonetise(ff.read(), arabic=False)
            phonemes = FeatureExtractor(d).get_features()
        temp_path = "temp.wav"
        for interval, phoneme in zip(intervals, phonemes):
            minTime = interval.minTime
            maxTime = interval.maxTime
            FileLoader.cut(wav_path, minTime, maxTime, temp_path)
            x, fs = sf.read(temp_path)
            f0, sp, ap = pw.wav2world(x, fs, frame_period=FeatureReader.frame_length)
            num_of_frames = int(math.ceil((maxTime - minTime) / float(FeatureReader.frame_length)))
            # print(num_of_frames)
            for frame, f, s, a in zip(range(1, num_of_frames + 1), f0, sp, ap):
                features = [frame] + phoneme
                # print(features)
                outpu = [f] + s + a
                features = np.concatenate((features, outpu))
                # print(len(features))
                file.write(",".join(list(map(str, features))) + "\n")
            # mfcc_feat = mfcc(sig, rate)
            # d_mfcc_feat = delta(mfcc_feat, 2)
            # fbank_feat = logfbank(sig, rate)
            # mfcc_feat = list(np.reshape(mfcc_feat, mfcc_feat.shape[0] * mfcc_feat.shape[1]))
            # d_mfcc_feat = list(np.reshape(d_mfcc_feat, d_mfcc_feat.shape[0] * d_mfcc_feat.shape[1]))
            # fbank_feat = list(np.reshape(fbank_feat, fbank_feat.shape[0] * fbank_feat.shape[1]))
            # additional_features = [maxTime - minTime]
            # all = phoneme + mfcc_feat + d_mfcc_feat + fbank_feat + additional_features
            # result.append(all)
            os.system("rm {}".format(temp_path))
            # self.data = result

    @staticmethod
    def cut(wav_path, minTime, maxTime, temp_path):
        command = "sox {} {} trim {} ={}".format(wav_path, temp_path, minTime, maxTime)
        os.system(command)
        return wav.read(temp_path)
