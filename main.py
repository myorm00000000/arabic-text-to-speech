from features.features_writer import FeaturesWriter
from features.feature_writer import FeatureWriter
from duration.duration_writer import DurationWriter
from duration.durations_writer import DurationsWriter
from nltk.tag.stanford import StanfordPOSTagger


def main():
    pass
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
    # path_to_corpus = "/home/obada/corpus"
    # feature_path = "/home/obada/durations.txt"
    # file_writer = DurationWriter()
    # writer = DurationsWriter(file_writer, path_to_corpus, feature_path)
    # writer.write()
    # tagger_path = "/home/obada/Downloads/stanford-postagger-full-2016-10-31/models/arabic.tagger"
    # jar_path = "/home/obada/Downloads/stanford-postagger-full-2016-10-31/stanford-postagger.jar"
    # st = StanfordPOSTagger(model_filename=tagger_path, path_to_jar=jar_path)
    # tags = st.tag('ماذا تفعل؟'.split())
    # for tag in tags:
    #     print(tag[1].split("/")[1])

    # data = loader.get_data()
    # with open("/home/obada/features.txt", "w") as f:
    #    for row in data:
    #        f.write(",".join(row))
    # path_to_trained_model = "model.h5"
    # data = FeatureReader.read(feature_path)
    # trainer = Trainer(data, StaticSplitter(num_of_out_features=len(data[0]) - 8))
    # trainer.train()
    # trainer.evaluate()
    # trainer.save_model(path_to_trained_model)


main()
