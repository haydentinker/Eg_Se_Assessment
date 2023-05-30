import pandas as pd
import pyarrow.parquet as pyarrow
import matplotlib.pyplot as plt
import numpy as np
from point_in_polygon import get_edges, is_inside


class ProcessGameState:
    ### ProcessGameState class.
    ### Takes in a file path to a paraquet file and an area_of_interest that is a list of points
    def __init__(self, file_path, area_of_interest):
        self.file_path = file_path
        self.edges = get_edges(area_of_interest)
        self.df = self.read_file()
        self.weapon_classes = set(
            j["weapon_class"]
            for inventory in self.df["inventory"].dropna()
            for j in inventory
        )
        self.within_area_df = self.filter_df_within_area()

    def read_file(self):
        ### Reads the paraquet file and cleans data
        ### Also looks at player's inventory to extract weapon classes and puts it into set
        table = pyarrow.read_table(self.file_path)
        df = table.to_pandas()
        print(df.area_name.unique())
        print(len(df.index))
        return df

    def filter_df_within_area(self):
        # Create a boolean mask for the z condition
        valid_z = (self.df["z"] >= 285) & (self.df["z"] <= 421)
        # Create a boolean mask for the is_inside condition
        valid_position = self.df.apply(
            lambda row: is_inside((row["x"], row["y"]), self.edges), axis=1
        )
        return self.df[valid_z & valid_position]

    def common_strategy(self, team="Team2", side="T"):
        ##Takes in a team and a side and checks whether entering the area of interest in a common strategy
        ##Will default to Team2 and T if team and side is not passed in.
        ##Returns a string with the percentage  of time the team is within the area of interest
        strategy_df = self.within_area_df.where(
            (self.within_area_df.team == team) & (self.within_area_df.side == side)
        ).dropna()
        return f"{len(strategy_df)/len(((self.df.team==team) & (self.df.side==side)).dropna()):.5%}"

    def average_time(self, area_name, team, side):
        # Filter the data for the specified area
        has_smg = self.df.apply(lambda row: has_smgs(row["inventory"]), axis=1)
        filtered_df = self.df[(self.df["area_name"] == area_name) & (has_smg)]

        average_time = filtered_df["seconds"].mean()

        print(
            f"The average time where at least two players are holding SMGs in {area_name} is: {average_time}"
        )

    def create_heat_map(self, location, team="Team2", side="CT"):
        location_df = self.df.where(
            (self.df.team == team)
            & (self.df.side == side)
            & (self.df.area_name == location)
        ).dropna()

        # Check if there are data points to create the heatmap
        if location_df.empty:
            print("No data points found for the specified location.")
            return

        num_bins_x = 50
        num_bins_y = 50

        # Compute the range based on the minimum and maximum values in the dataset
        x_min, x_max = location_df["x"].min(), location_df["x"].max()
        y_min, y_max = location_df["y"].min(), location_df["y"].max()

        # Compute the 2D histogram
        hist, x_edges, y_edges = np.histogram2d(
            location_df["x"].values,
            location_df["y"].values,
            bins=(num_bins_x, num_bins_y),
            range=((x_min, x_max), (y_min, y_max)),
        )
        grid = hist.T

        # Plot the heatmap
        plt.figure(figsize=(10, 8))  # Adjust the figure size as needed
        heatmap = plt.imshow(grid, cmap="jet", interpolation="lanczos")

        # Add gridlines
        plt.grid(which="major", axis="both", linestyle="-", color="k", linewidth=1)

        # Add a colorbar
        plt.colorbar(heatmap)

        # Set appropriate labels and title
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Heatmap: {} - {} - {}".format(location, team, side))

        # Display the plot
        plt.show()


def has_smgs(inventory):
    if inventory is None:
        return False
    for item in inventory:
        if item["weapon_class"] == "SMG":
            return True
    return False
