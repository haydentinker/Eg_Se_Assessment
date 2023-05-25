import pandas as pd

# [-1735, 250]
# [-2024, 398]
# [-2806, 742]
# [-2472, 1233]
# [-1565, 580]


class ProcessGameState:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.read_file()
        self.area_of_interest = [
            (-1735, 250),
            (-2024, 398),
            (-2806, 742),
            (-2472, 1233),
            (-1565, 580),
        ]
        # self.area_of_interest = area_of_interest

    def read_file(self):
        self.df = pd.read_parquet(self.file_path, engine="fastparquet")
        self.df.to_csv("./data/dfToCSV.csv", index=False)
        mask = pd.Series([False] * len(self.df))
        for i in range(len(self.df)):
            mask[i] = self.is_inside((self.df[i]["x"], self.df[i]["y"]))
        self.df = self.df[mask]
        print(len(self.df.index))

    def is_inside(self, point):
        x, y = point
        n = len(self.area_of_interest)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters(y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
        return inside
