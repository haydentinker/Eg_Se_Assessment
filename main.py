from process_game_state import ProcessGameState
import pandas as pd
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
    et = time.time()
    time1 = et - st
    print("Time:", time1)


if __name__ == "__main__":
    main()
