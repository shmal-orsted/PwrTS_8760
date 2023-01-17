"""
Power Time Series project
Author: Shawn Malone, Clay Matheny, Meghan Mitchell
1/6/2023

Revised Version of Clay's Code removing labor intensive work and preprocessing of data files
"""
import pandas as pd
from functions import losses_parser, startup, windfarmer_process, power_time_series, losses_app, import_data, export
import os


def main():
    '''
    Starting with data imported and filepaths brought in
    '''
    # import input filepaths
    working_dir = os.getcwd()
    filepaths = startup.main(working_dir)

    # import windog, windfarmer and losses data
    windog_data, windog_data_headers = import_data.import_windog(filepaths["windog"])
    windfarmer_data = import_data.import_windfarmer(filepaths["windfarmer"])
    losses = losses_parser.main(filepaths["losses"])

    # processing data and making adjustments before pwts is made
    windfarmer_sectors = windfarmer_process.main(windfarmer_data)

    # Making the power time series
    pwts, is_8760 = power_time_series.main(windfarmer_sectors, windog_data, windog_data_headers)

    # Apply losses to the power time series
    pwts, total_loss, sum_power, losses_sum = losses_app.main(pwts, losses)

    export.export_csv(pwts, working_dir, is_8760)
    export.peer_review_print(is_8760, total_loss, sum_power, losses_sum)

    return pwts, is_8760


pwts_finished = main()

pass