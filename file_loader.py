import os

import numpy as np
import scipy.io.wavfile as wav
from python_speech_features import delta
from python_speech_features import logfbank
from python_speech_features import mfcc
from textgrid import TextGrid

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
        temp_path = "/home/obada/temp.wav"
        for interval, phoneme in zip(intervals, phonemes):
            minTime = interval.minTime
            maxTime = interval.maxTime
            rate, sig = FileLoader.cut(wav_path, minTime, maxTime, temp_path)
            mfcc_feat = mfcc(sig, rate)
            d_mfcc_feat = delta(mfcc_feat, 2)
            fbank_feat = logfbank(sig, rate)
            mfcc_feat = list(np.reshape(mfcc_feat, mfcc_feat.shape[0] * mfcc_feat.shape[1]))
            d_mfcc_feat = list(np.reshape(d_mfcc_feat, d_mfcc_feat.shape[0] * d_mfcc_feat.shape[1]))
            fbank_feat = list(np.reshape(fbank_feat, fbank_feat.shape[0] * fbank_feat.shape[1]))
            additional_features = [maxTime - minTime]
            all = phoneme + mfcc_feat + d_mfcc_feat + fbank_feat + additional_features
            file.write(",".join(list(map(str, all))) + "\n")
            # result.append(all)
            os.system("rm {}".format(temp_path))
        # self.data = result

    @staticmethod
    def cut(wav_path, minTime, maxTime, temp_path):
        command = "sox {} {} trim {} ={}".format(wav_path, temp_path, minTime, maxTime)
        os.system(command)
        return wav.read(temp_path)

