# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 20:01:11 2024

@author: liulu
"""

import os
import pandas as pd

def process_csv(file_path, max_rows=100):
    # read CSV
    df = pd.read_csv(file_path)

    # row > max_rows，save the number of max_rows
    if len(df) > max_rows:
        df = df.iloc[:max_rows]

    # save the worked files
    df.to_csv(file_path, index=False)
    print(f"Processed file: {file_path}")

def find_and_process_files(root_dir, file_name='polar.csv'):
    # Traversing a directory to find a file
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file == file_name:
                file_path = os.path.join(subdir, file)
                process_csv(file_path)

# specify the root direction
root_directory = r'file_path'
find_and_process_files(root_directory)
