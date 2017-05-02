from nltk.tag.stanford import StanfordPOSTagger
from phoneme.phonetise import buckwalterToArabic

consonants = [
    "r", "g", "y", "G",
    "b", "z", "f", "v",
    "t", "s", "q", "p",
    "$", "k", "<",
    "j", "S", "l",
    "H", "D", "m",
    "x", "T", "n",
    "d", "Z", "h",
    "*", "E", "w", "^"]
geminatedConsonants = [
    "<<", "rr", "gg", "vv",
    "bb", "zz", "ff", "GG",
    "tt", "ss", "qq", "pp",
    "$$", "kk", "yy",
    "jj", "SS", "ll",
    "HH", "DD", "mm",
    "xx", "TT", "nn",
    "dd", "ZZ", "hh",
    "**", "EE", "ww", "^^"]
longVowels = ["aa", "AA",
              "uu0", "uu1",
              "ii0", "ii1",
              "UU0", "UU1",
              "II0", "II1"]
shortVowels = ["a", "A",
               "u0", "u1",
               "i0", "i1",
               "U0", "U1",
               "I0", "I1"]
tags_type = ["CC", "CD", "CONJ+NEG_PART", "DT", "FW", "IN", "JJ", "NN", "NNP", "NNPS", "NNS", "NO_FUNC",
             "NUMERIC_COMMA", "PRP", "PRP$", "PUNC", "RB", "UH", "VBD", "VBN", "VBP", "WP", "WRB"]


class FeatureExtractor:
    def __init__(self, data):
        result = []
        t = [item for sublist in data for item in sublist]
        syllable = FeatureExtractor.syllabify(t)
        indices = FeatureExtractor.divide(syllable)
        tagger_path = "/home/obada/Downloads/stanford-postagger-full-2016-10-31/models/arabic.tagger"
        jar_path = "/home/obada/Downloads/stanford-postagger-full-2016-10-31/stanford-postagger.jar"
        st = StanfordPOSTagger(model_filename=tagger_path, path_to_jar=jar_path)
        temp = list(map("".join, data))
        arabic = ""
        for i in temp:
            arabic += i + " "
        arabic = buckwalterToArabic(arabic.strip())
        tags = st.tag(arabic)
        tags = [i[1].split("/")[1] for i in tags]
        for tag in tags:
            print(tag[1].split("/")[1])
        for i, tag in zip(data, tags):
            tag_index = tags_type.index(tag)
            one_hot_tag_index = [0] * len(tags_type)
            one_hot_tag_index[tag_index] = 1
            # syllable = FeatureExtractor.syllabify(data[i])
            # indices = FeatureExtractor.divide(syllable)
            for j in range(0, len(i)):
                phone = i[j].replace('\'', '')
                syllab_index, phone_index = FeatureExtractor.phone_in_syllable(indices, j)
                result.append([1 if phone in consonants else 0,
                               1 if phone in shortVowels else 0,
                               1 if phone in longVowels else 0,
                               1 if phone in geminatedConsonants else 0,
                               1 if i[j][-1] == '\'' else 0,  # stressed
                               j,
                               1 if j < len(i) - 1 and i[j + 1][-1] == '\'' else 0,  # next stressed
                               1 if j > 0 and i[j - 1][-1] == '\'' else 0,  # prev stressed
                               syllab_index,
                               phone_index]
                              + one_hot_tag_index)
        self.features = result

    @staticmethod
    def syllabify(sequence):
        syllable = ""
        for i in sequence:
            t = i.replace('\'', '')
            if t in geminatedConsonants:
                syllable += "cc"
            elif t in consonants:
                syllable += "c"
            elif t in longVowels:
                syllable += "vv"
            else:
                syllable += "v"
        return syllable

    @staticmethod
    def divide(syllab):
        temp = syllab
        length = len(syllab)
        acc = 0
        types = ["cvvcc", "cvcc", "cvvc", "cvc", "cvv", "cv"]
        indices = []
        while len(temp) != 0:
            index = FeatureExtractor.get_index(temp, types)
            acc += index
            indices.append(length - acc)
            temp = temp[:-index]
        indices.reverse()
        return indices

    @staticmethod
    def phone_in_syllable(indices, index):
        if len(indices) == 1:
            return 0, index
        for i in range(0, len(indices) - 1):
            if indices[i] <= index <= indices[i + 1]:
                return i, index - indices[i]
        return len(indices) - 1, index - indices[len(indices) - 1]

    @staticmethod
    def get_index(syllab, types):
        for t in types:
            if syllab.endswith(t):
                return len(t)
        return 0

    def get_features(self):
        return self.features
