# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 20:01:11 2024

@author: liulu
"""

import os
import pandas as pd
import numpy as np

def downsample_csv(file_path, max_rows=100):
    df = pd.read_csv(file_path)

    if len(df) > max_rows:
        indices = np.linspace(0, len(df) - 1, max_rows, dtype=int)
        df = df.iloc[indices]

    # save
    df.to_csv(file_path, index=False)
    print(f"Processed file: {file_path}")

def find_and_process_files(root_dir, file_name='polar.csv'):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file == file_name:
                file_path = os.path.join(subdir, file)
                downsample_csv(file_path)

# specify the root direction
root_directory = r'D:\Machine learning Project\data' 
find_and_process_files(root_directory)
