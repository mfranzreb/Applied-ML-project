import os
import matplotlib.pyplot as plt
import numpy as np


def find():
    train_folder = os.path.join(os.getcwd(), "data", "train")
    test_folder = os.path.join(os.getcwd(), "data", "test")

    min_cl = 100
    max_cl = 0
    min_cd = 100
    max_cd = 0
    # Iterate through each subfolder
    for subfolder in os.listdir(train_folder):
        subfolder_path = os.path.join(train_folder, subfolder)
        data_file = os.path.join(subfolder_path, "polar.csv")
        cl, cd = np.loadtxt(data_file, delimiter=",", unpack=True, skiprows=1)
        min_cl = min(min_cl, min(cl))
        max_cl = max(max_cl, max(cl))
        min_cd = min(min_cd, min(cd))
        max_cd = max(max_cd, max(cd))

    for subfolder in os.listdir(test_folder):
        subfolder_path = os.path.join(test_folder, subfolder)
        data_file = os.path.join(subfolder_path, "polar.csv")
        cl, cd = np.loadtxt(data_file, delimiter=",", unpack=True, skiprows=1)
        min_cl = min(min_cl, min(cl))
        max_cl = max(max_cl, max(cl))
        min_cd = min(min_cd, min(cd))
        max_cd = max(max_cd, max(cd))

    print(f"Min CL: {min_cl}, Max CL: {max_cl}")
    print(f"Min CD: {min_cd}, Max CD: {max_cd}")


if __name__ == "__main__":
    find()
