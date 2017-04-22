import os

from file_loader import FileLoader


class DataLoader:
    def __init__(self, l, base_path, file_path):
        wav_base = base_path + "/wav/"
        grid_base = base_path + "/textgrid/"
        text_base = base_path + "/lab/"
        ite = zip(sorted(os.listdir(wav_base)), sorted(os.listdir(grid_base)), sorted(os.listdir(text_base)))
        with open(file_path, "w") as file:
            for wav, grid, text in ite:
                print(wav)
                l.load(wav_path=wav_base + wav, text_path=text_base + text, grid_path=grid_base + grid, file=file)


if __name__ == "__main__":
    f = FileLoader()
    loader = DataLoader(f, "/home/obada/corpus")
    print("finished")
    # print(loader.get_data())
