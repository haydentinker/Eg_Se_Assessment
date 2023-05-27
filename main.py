import pandas as pd
from process_game_state import ProcessGameState
import time


def main():
    st = time.time()
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
    print(gameState.common_strategy())
    et = time.time()
    time1 = et - st
    print("Time:", time1)
    print(gameState.weapon_classes)


if __name__ == "__main__":
    main()
