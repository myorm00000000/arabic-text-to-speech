import os


class FeaturesWriter:
    def __init__(self, w, base_path, file_path):
        self.file_path = file_path
        self.base_path = base_path
        self.writer = w

    def write(self):
        wav_base = self.base_path + "/wav/"
        grid_base = self.base_path + "/textgrid/"
        text_base = self.base_path + "/lab/"
        ite = zip(sorted(os.listdir(wav_base)), sorted(os.listdir(grid_base)), sorted(os.listdir(text_base)))
        with open(self.file_path, "w") as file:
            for wav, grid, text in ite:
                self.writer.write(wav_path=wav_base + wav, text_path=text_base + text, grid_path=grid_base + grid, file=file)
