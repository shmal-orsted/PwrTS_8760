"""
Power Time Series project
Author: Shawn Malone, Clay Matheny
1/6/2023

Revised Version of Clay's Code removing labor intensive work and preprocessing of data files
"""
import pandas as pd
from functions import losses_parser, startup
import os


def main():
    '''
    Starting with data imported and filepaths brought in
    '''
    # import input filepaths
    working_dir = os.getcwd()
    filepaths = startup.main(working_dir)

    # import windog, windfarmer and losses data
    windog_data = import_windog(filepaths["windog"])
    windfarmer_data = import_windfarmer(filepaths["windfarmer"])
    losses = losses_parser.main(filepaths["losses"])

    return filepaths, windog_data, windfarmer_data, losses


def import_windog(windog_filepath):
    # importing windog data
    windog_data = pd.read_csv(windog_filepath, sep='\t')
    # convert first column to datetime
    windog_data["Timestamp"] = pd.to_datetime(windog_data["Timestamp"], format="%m/%d/%Y %H:%M")
    return windog_data


def import_windfarmer(windfarmer_filepath):
    # importing and manipulating windfarmer data into usable format
    windfarmer_dataset = pd.read_csv(windfarmer_filepath, sep='\t', header=9)
    windfarmer_dataset = windfarmer_dataset.set_index("Unnamed: 0")
    return windfarmer_dataset


filepaths, windog_data, windfarmer_data, losses = main()
pass