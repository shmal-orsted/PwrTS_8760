"""
Power Time Series project
Author: Shawn Malone, Clay Matheny
1/6/2023

Revised Version of Clay's Code removing labor intensive work and preprocessing of data files
"""
import pandas as pd
import glob, os
import losses_parser, startup


def main():
    '''
    Starting with data imported and filepaths brought in
    '''
    # import input filepaths
    filepaths = startup.main()

    # Working windfarmer data into usable format
    mydataset2 = pd.read_csv(filepaths["Windfarmer"], sep='\t', header=9)
    mydataset2 = mydataset2.set_index("Unnamed: 0")

    losses = losses_parser.main(filepaths["Losses"])
    if not bool(losses):
        raise Exception("Losses file imported incorrectly")
    return filepaths, mydataset2, losses

# find ini file and add to directory

filepaths, mydataset2, losses = main()
pass