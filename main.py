"""
Power Time Series project
Author: Shawn Malone, Clay Matheny, Meghan Mitchell
1/6/2023

Revised Version of Clay's Code removing labor intensive work and preprocessing of data files
Adds tmy generation, scaling mean of momm to site wind speed, grid curtailment, temperature derating
"""
import pandas as pd
from functions import startup_parser, losses_parser, startup, windfarmer_process, power_time_series, \
    losses_app, import_data, export, scaling
import os


def main():
    '''
    Starting with data imported and filepaths brought in
    '''
    # import input filepaths
    working_dir = os.getcwd()
    filepaths = startup.main(working_dir)
    #import startup parameters
    startup_params = startup_parser.main(working_dir, filepaths["startup"])

    # import windog, windfarmer and losses data
    #if there is no txt file in the inputs folder default to the tmy branch of the code to make a tmy dataset
    windog_data, windog_data_headers = import_data.import_windog(filepaths["windog"], startup_params, working_dir)

    windfarmer_data = import_data.import_windfarmer(filepaths["windfarmer"])
    losses = losses_parser.main(filepaths["losses"])

    # processing data and making adjustments before pwts is made
    windfarmer_sectors = windfarmer_process.main(windfarmer_data)

    # scaling the wind data to a input value, if applicable
    windog_data, momm = scaling.main(windog_data, startup_params, windog_data_headers)

    # Making the power time series
    pwts, is_8760 = power_time_series.main(windfarmer_sectors, windog_data, windog_data_headers, startup_params)

    # Apply losses to the power time series
    pwts, bulk_loss = losses_app.main(pwts, losses, windog_data_headers, startup_params, working_dir)

    export.export_csv(pwts, working_dir, is_8760)
    export.peer_review_print(pwts, is_8760, bulk_loss, working_dir)

    return


pwts_finished = main()

pass