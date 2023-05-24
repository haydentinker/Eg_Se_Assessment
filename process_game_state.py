import pandas as pd


class ProcessGameState:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.read_file()

    def read_file(self):
        self.df = pd.read_parquet(self.file_path, engine="fastparquet")
        print(self.df)
