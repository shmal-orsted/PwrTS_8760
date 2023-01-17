"""
Power Time Series project
Author: Shawn Malone, Clay Matheny, Meghan Mitchell
1/6/2023

Revised Version of Clay's Code removing labor intensive work and preprocessing of data files
"""
import pandas as pd
from functions import losses_parser, startup, windfarmer_process, power_time_series, losses_app
import os


def main():
    '''
    Starting with data imported and filepaths brought in
    '''
    # import input filepaths
    working_dir = os.getcwd()
    filepaths = startup.main(working_dir)

    # import windog, windfarmer and losses data
    windog_data, windog_data_headers = import_windog(filepaths["windog"])
    windfarmer_data = import_windfarmer(filepaths["windfarmer"])
    losses = losses_parser.main(filepaths["losses"])

    # processing data and making adjustments before pwts is made
    windfarmer_sectors = windfarmer_process.main(windfarmer_data)

    # Making the power time series
    pwts, is_8760 = power_time_series.main(windfarmer_sectors, windog_data, windog_data_headers)

    # Apply losses to the power time series
    pwts = losses_app.main(pwts, losses)

    return pwts, is_8760


def import_windog(windog_filepath):

    windog_data_headers_dict = {}

    # importing windog data
    windog_data = pd.read_csv(windog_filepath, sep='\t')
    # convert first column to datetime
    windog_data["Timestamp"] = pd.to_datetime(windog_data["Timestamp"], format="%m/%d/%Y %H:%M")
    # Upon import, set references to columns and remove hard coded names throughout code
    # Get list of column headers
    windog_data_headers = windog_data.columns.values.tolist()

    # Identify Dir, Spd and Timestamp columns
    for header in windog_data_headers:
        if "Spd" in header:
            windog_data_headers_dict["speed"] = header
        elif "Dir" in header:
            windog_data_headers_dict["direction"] = header
        elif "Timestamp" in header:
            windog_data_headers_dict["timestamp"] = header

    return windog_data, windog_data_headers_dict


def import_windfarmer(windfarmer_filepath):
    # importing and manipulating windfarmer data into usable format
    windfarmer_dataset = pd.read_csv(windfarmer_filepath, sep='\t', header=9)
    windfarmer_dataset = windfarmer_dataset.set_index("Unnamed: 0")
    return windfarmer_dataset


pwts_finished = main()
pass