import os
import matplotlib.pyplot as plt
import numpy as np


def plot_and_save(folder_path):
    # Read geometrical information
    if os.path.exists(os.path.join(folder_path, "polar_plot.png")):
        return
    data_file = os.path.join(folder_path, "polar.csv")
    y, x = np.loadtxt(data_file, delimiter=",", unpack=True, skiprows=1)

    min_x = 0.0
    max_x = 0.55
    min_y = -1.8
    max_y = 2.55

    # Plot and save image
    plt.figure(figsize=(3, 3), dpi=100)  # Adjust the figure size as needed
    # plt.scatter(x, y, color='none', marker='.')
    plt.plot(
        x, y, color="black", linestyle="-", linewidth=1
    )  # Connect points with a red spline
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.axis("off")  # Remove axis
    fig = plt.gcf()
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    image_path = os.path.join(folder_path, "polar_plot.png")
    # plt.savefig(image_path, bbox_inches="tight", pad_inches=0, cmap="gray")
    plt.imsave(image_path, data, cmap="gray")
    # plt.show()
    plt.close()

    # print(f"Image saved at: {image_path}")


train_folder = os.path.join(os.getcwd(), "data", "train")
test_folder = os.path.join(os.getcwd(), "data", "test")


# Iterate through each subfolder
for subfolder in os.listdir(train_folder):
    subfolder_path = os.path.join(train_folder, subfolder)

    if os.path.isdir(subfolder_path):
        plot_and_save(subfolder_path)

for subfolder in os.listdir(test_folder):
    subfolder_path = os.path.join(test_folder, subfolder)

    if os.path.isdir(subfolder_path):
        plot_and_save(subfolder_path)
