# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 20:17:28 2024

@author: liulu
"""

import os
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

def linear_interpolate_df(df, target_rows=100):
    # the number of row
    num_rows = len(df)
    print(num_rows)

    if num_rows >= target_rows:
        return df

    # interpolation of the data which is smaller than 101
    new_index = np.linspace(0, num_rows - 1, target_rows)
    interpolated_data = {col: interp1d(range(num_rows), df[col], kind='linear')(new_index) for col in df.columns}

    # create new DataFrame
    new_df = pd.DataFrame(interpolated_data)
    return new_df

def process_csv(file_path, max_rows=101):
    df = pd.read_csv(file_path)

    # Add the Interpolation value in the row
    df = linear_interpolate_df(df, max_rows)

    # Save the data
    df.to_csv(file_path, index=False)
    print(f"Processed file: {file_path}")

def find_and_process_files(root_dir, file_name='polar.csv'):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file == file_name:
                file_path = os.path.join(subdir, file)
                process_csv(file_path)

# specify the root direction
root_directory = r'file_path'
find_and_process_files(root_directory)
