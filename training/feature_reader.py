class FeatureReader:
    @staticmethod
    def read(file_path):
        res = []
        with open(file_path, "r") as f:
            lines = f.read().split("\n")
            for line in lines:
                if line != '':
                    res.append(list(map(float, line.split(","))))
        return res
