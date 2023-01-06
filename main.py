"""
Power Time Series project
Author: Shawn Malone, Clay Matheny
1/6/2023

Revised Version of Clay's Code removing labor intensive work and preprocessing of data files

"""

import pandas as pd
import glob, os

# import FPM file correctly without preprocessing

files = []

# find input directory folder
for file in os.listdir("./inputs"):
    if file.endswith(".fpm"):
        files.append(file)

mydataset2 = pd.read_csv(f"./inputs/{files[0]}", sep='\t', header=9)
mydataset2 = mydataset2.set_index("Unnamed: 0")
pass