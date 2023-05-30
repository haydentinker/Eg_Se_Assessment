import pandas as pd
from process_game_state import ProcessGameState


def main():
    gameState = ProcessGameState(
        "./data/game_state_frame_data.parquet",
        [
            (-1735, 250),
            (-2024, 398),
            (-2806, 742),
            (-2472, 1233),
            (-1565, 580),
        ],
    )
    print(f"How often team enters the boundary:{gameState.common_strategy()}")
    print(f"Weapon Classes: {gameState.weapon_classes}")
    gameState.average_time("BombsiteB", "Team2", "T")
    print("Generating Heat Map")
    gameState.create_heat_map("BombsiteB")


if __name__ == "__main__":
    main()
