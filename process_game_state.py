import pandas as pd
import pyarrow.parquet as pyarrow


class ProcessGameState:
    ### ProcessGameState class.
    ### Takes in a file path to a paraquet file and an area_of_interest that is a list of points
    def __init__(self, file_path, area_of_interest):
        self.file_path = file_path
        self.edges = get_edges(area_of_interest)
        self.df = self.read_file()
        self.weapon_classes = set()

    def read_file(self):
        ### Reads the paraquet file then filters based on area_of_interest
        ### Also looks at player's inventory to extract weapon classes and puts it into set
        table = pyarrow.read_table("./data/game_state_frame_data.parquet")
        df = table.to_pandas()
        weapon_classes = set()
        mask = pd.Series([False] * len(df))
        for i in range(len(df)):
            if df.at[i, "inventory"] is not None:
                for j in df.at[i, "inventory"]:
                    weapon_classes.add(j["weapon_class"])
            if (df.at[i, "z"] < 285) | (df.at[i, "z"] > 421):
                continue
            mask[i] = is_inside((df.at[i, "x"], df.at[i, "y"]), self.edges)
        df = df[mask]
        print(len(df.index))
        print(weapon_classes)
        return df


def is_inside(point, edges):
    # Checks to see if a point is within a polygon
    xp, yp = point
    count = 0
    for edge in edges:
        (x1, y1), (x2, y2) = edge
        if (yp < y1) != (yp < y2) and xp < x1 + ((yp - y1) / (y2 - y1) * (x2 - x1)):
            count += 1
    return count % 2 == 1


def get_edges(area_of_interest):
    # Creates edges based on a list of points
    edges = []
    for i in range(0, len(area_of_interest)):
        if i != len(area_of_interest) - 1:
            edges.append((area_of_interest[i], area_of_interest[i + 1]))
        else:
            edges.append((area_of_interest[i], area_of_interest[0]))
    return edges
