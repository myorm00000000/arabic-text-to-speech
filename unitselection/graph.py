class Graph:
    def __init__(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
        vectors = []
        indices = []
        index = 0
        for i in range(1, len(lines)):
            if lines[i] == "indices:":
                index = i + 1
                break
            parts = lines[i].split(":")
            vectors.append((parts[0], list(map(float, parts[1].split(",")))))
        for j in range(index, len(lines)):
            indices.append(list(map(float, lines[j].split(","))))
        self.edges = zip(vectors, indices)

