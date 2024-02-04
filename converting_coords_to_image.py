import os
import matplotlib.pyplot as plt
import numpy as np

def plot_and_save(folder_path):
    # Read geometrical information
    data_file = os.path.join(folder_path, "coords.csv")
    x, y = np.loadtxt(data_file, delimiter=',', unpack=True, skiprows=1)

    # Plot and save image
    plt.figure(figsize=(8, 8))  # Adjust the figure size as needed
    #plt.scatter(x, y, color='none', marker='.')
    plt.scatter(x, y, color='blue', marker='.')
    plt.plot(x, y, color='red', linestyle='-', linewidth=2)  # Connect points with a red spline
    plt.axis('equal')  # Equal scaling for x and y axes
    plt.axis('off')  # Remove axis
    plt.xticks([])  # Hide x-axis ticks and labels
    plt.yticks([])  # Hide y-axis ticks and labels

    #image_path = os.path.join(folder_path, "geometrical_plot.png")
    image_path = os.path.join(folder_path, "geometrical_plot_with_scatter.png")
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    print(f"Image saved at: {image_path}")

#main_folder = r'C:\Users\gloom\Documents\GitHub\AML\data\test'
main_folder = r'C:\Users\gloom\Documents\GitHub\Applied-ML-project\data\train'

# Iterate through each subfolder
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    if os.path.isdir(subfolder_path):
        plot_and_save(subfolder_path)
