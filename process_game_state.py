import pandas as pd


class ProcessGameState:
    def __init__(self, file_path, area_of_interest):
        self.file_path = file_path
        self.edges = get_edges(area_of_interest)
        self.df = self.read_file()

    def read_file(self):
        df = pd.read_parquet(self.file_path, engine="fastparquet")
        mask = pd.Series([False] * len(df))
        for i in range(len(df)):
            mask[i] = self.is_inside((df.at[i, "x"], df.at[i, "y"]), self.edges)
        df = df[mask]
        df.to_csv("./data/dfToCSV.csv", index=False)
        print(len(df.index))
        return df


def is_inside(point, edges):
    xp, yp = point
    count = 0
    for edge in edges:
        (x1, y1), (x2, y2) = edge
        if (yp < y1) != (yp < y2) and xp < x1 + ((yp - y1) / (y2 - y1) * (x2 - x1)):
            count += 1
    return count % 2 == 1


def get_edges(area_of_interest):
    edges = []
    for i in range(0, len(area_of_interest)):
        if i != len(area_of_interest) - 1:
            edges.append((area_of_interest[i], area_of_interest[i + 1]))
        else:
            edges.append((area_of_interest[i], area_of_interest[0]))
    return edges
