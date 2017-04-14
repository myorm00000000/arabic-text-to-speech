from data_loader import DataLoader

from file_loader import FileLoader
from splitter.static_splitter import StaticSplitter
from training.trainer import Trainer
from training.feature_reader import FeatureReader


def main():
    # np.random.seed(123151)
    # trainer = Trainer(DataLoader(FileLoader, "/home/obada/corpus"), StaticSplitter())
    # trainer.train()
    # train_error, test_error = trainer.evaluate()
    # print("Train Error = {}\n".format(train_error))
    # print("Test Error = {}\n".format(test_error))
    # (a, b, c, d) = phonetise(
    #     "فَقَالَ الْجُمْهُورُِ")
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # with open("/home/obada/data.txt", "r") as f:
    #     lines = f.read().split("\n")
    #     data = []
    #     for line in lines:
    #         if line != '':
    #             l = line.split(",")
    #             data.append([float(l[0]), float(l[1]), float(l[2]), float(l[3]), float(l[4])])
    # FileLoader.acoustic_features_length = 1
    # trainer = Trainer(data, StaticSplitter())
    # path_to_corpus = "corpus"
    # file_loader = FileLoader()
    # loader = DataLoader(file_loader, path_to_corpus, feature_path)
    # data = loader.get_data()
    # with open("/home/obada/features.txt", "w") as f:
    #    for row in data:
    #        f.write(",".join(row))
    path_to_trained_model = "model.h5"
    feature_path = "/home/obada/features.txt"
    data = FeatureReader.read(feature_path)
    trainer = Trainer(data, StaticSplitter(num_of_out_features=len(data[0]) - 8))
    #trainer.train()
    #trainer.evaluate()
    #trainer.save_model(path_to_trained_model)


main()
