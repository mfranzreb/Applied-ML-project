import os
import pandas as pd
import numpy as np
import subprocess
import time
import matplotlib.pyplot as plt


if __name__ == "__main__":
    source_folder = os.path.join(
        os.getcwd(), "data"
    )  # Replace with the actual path to your 'data' folder
    train_folder = os.path.join(source_folder, "train")
    subfolders = [f.path for f in os.scandir(train_folder) if f.is_dir()]
    # plot polars
    min = 1000
    max = 0
    for folder in subfolders:
        polars = pd.read_csv(os.path.join(folder, "polar.csv"))
        coords = pd.read_csv(os.path.join(folder, "coords.csv"))
        plt.plot(polars["Cd"], polars["Cl"], "o-")
        plt.show()
        plt.plot(coords["x"], coords["y"], "o-")
        plt.gca().set_aspect("equal", adjustable="box")
        plt.show()
        num_polars = polars.shape[0]
        if num_polars < min:
            min = num_polars
        if num_polars > max:
            max = num_polars

    print(min, max)
