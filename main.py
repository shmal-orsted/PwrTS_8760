"""
Power Time Series project
Author: Shawn Malone, Clay Matheny, Meghan Mitchell
1/6/2023

Revised Version of Clay's Code removing labor intensive work and preprocessing of data files
Adds tmy generation, scaling mean of momm to site wind speed, grid curtailment, temperature derating
"""
import pandas as pd
from functions import startup_parser, losses_parser, startup, windfarmer_process, power_time_series, \
    losses_app, import_data, export, scaling, twelvex24
import os


def main(fpm_filepath, losses_filepath, startup_params_filepath, txt_filepath, run_8760, working_dir, turbine_filepath):
    """
    Starting with data imported and filepaths brought in
    """
    # import input filepaths
    # working_dir = os.getcwd()
    # filepaths = startup.main(working_dir)

    # replace startup function with the filepaths from the interface inputs
    filepaths = {
        "windfarmer": fpm_filepath,
        "losses": losses_filepath,
        "startup": startup_params_filepath,
        "windog": txt_filepath

    }

    # import startup parameters
    startup_params = startup_parser.main(working_dir, filepaths["startup"])

    startup_params["turbine_model"] = turbine_filepath

    # use value from interface running 8760 or pwts
    startup_params["run_8760"] = run_8760

    # import windog, windfarmer and losses data
    windog_data, windog_data_headers = import_data.import_windog(filepaths["windog"], startup_params, working_dir)

    windfarmer_data = import_data.import_windfarmer(filepaths["windfarmer"])
    losses = losses_parser.main(filepaths["losses"])

    # processing data and making adjustments before pwts is made
    windfarmer_sectors = windfarmer_process.main(windfarmer_data)

    # scaling the wind data to a input value, if applicable
    if startup_params["run_8760"] is True:
        windog_data, momm = scaling.main(windog_data, startup_params, windog_data_headers)

    # Making the power time series
    pwts, is_8760 = power_time_series.main(windfarmer_sectors, windog_data, windog_data_headers, startup_params)

    # Apply losses to the power time series
    pwts, bulk_loss = losses_app.main(pwts, losses, windog_data_headers, startup_params, working_dir)

    # create 12x24 with 8760 time series
    if startup_params["run_8760"] is True:
        percent_twelvex24_df_net, twelvex24_df_net, percent_twelvex24_df_gross, twelvex24_df_gross, \
            pwts = twelvex24.main(pwts)
        export.export_12x24(percent_twelvex24_df_net, twelvex24_df_net, working_dir, "netpower")
        export.export_12x24(percent_twelvex24_df_gross, twelvex24_df_gross, working_dir, "grosspower")

    # export data
    # add pwts to exports
    export.export_csv(pwts, working_dir, startup_params["run_8760"])
    export.peer_review_print(pwts, startup_params["run_8760"], bulk_loss, working_dir)

    return


if __name__ == "__main__":
    main()
pass