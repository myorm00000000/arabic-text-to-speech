import pyworld as pw


class FeatureReader:
    frame_length = pw.default_frame_period

    @staticmethod
    def read(file_path):
        res = []
        with open(file_path, "r") as f:
            lines = f.read().split("\n")
            for line in lines:
                if line != '':
                    res.append(list(map(float, line.split(","))))
        return res
