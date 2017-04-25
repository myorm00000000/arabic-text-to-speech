import os


class PhonemesWriter:
    def __init__(self, base_path, file_path):
        super().__init__()
        self.base_path = base_path
        self.file_path = file_path

    def write(self):
        wav_base = self.base_path + "/wav/"
        grid_base = self.base_path + "/textgrid/"
        text_base = self.base_path + "/lab/"
        wavs = sorted(os.listdir(wav_base))
        grids = sorted(os.listdir(grid_base))
        texts = sorted(os.listdir(text_base))
        with open(self.file_path, "w") as file:
            for i in range(len(wavs)):
                wav = wavs[i]
                grid = grids[i]
                text = texts[i]
