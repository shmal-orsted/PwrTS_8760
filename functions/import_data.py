import pandas as pd
import numpy as np
from tmy import tmy_main

def import_windog(windog_filepath, startup_params, working_dir):

    windog_data_headers_dict = {}

    # TMY will engage here if startup_params["run_8760"] = True
    if startup_params["run_8760"] is True:
        print("run_8760 is True, running TMY and 8760 process")
        windog_data, windog_data_headers = tmy_main.main(windog_filepath, working_dir)
    else:
        # importing windog data
        windog_data = pd.read_csv(windog_filepath, sep='\t')
        # convert first column to datetime
        windog_data["Timestamp"] = pd.to_datetime(windog_data["Timestamp"], format="%m-%d-%Y %H:%M")

        # add month and year values for analysis
        windog_data = windog_data.set_index(["Timestamp"])
        windog_data["Month"] = windog_data.index
        windog_data["Month"] = windog_data["Month"].apply(lambda x: x.month)
        windog_data["Year"] = windog_data.index
        windog_data["Year"] = windog_data["Year"].apply(lambda x: x.year)
        windog_data = windog_data.reset_index()


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
        elif "Tmp" in header:
            windog_data_headers_dict["temperature"] = header

    # replacing invalid values with NaNs for functions
    windog_data[windog_data_headers_dict["direction"]] = windog_data[windog_data_headers_dict["direction"]].replace(
        9999, np.NaN)
    windog_data[windog_data_headers_dict["temperature"]] = windog_data[
        windog_data_headers_dict["temperature"]].replace(
        9999, np.NaN)
    windog_data[windog_data_headers_dict["speed"]] = windog_data[windog_data_headers_dict["speed"]].replace(
        9999, np.NaN)
    windog_data[windog_data_headers_dict["direction"]] = windog_data[windog_data_headers_dict["direction"]].replace(
        -999999, np.NaN)
    windog_data[windog_data_headers_dict["temperature"]] = windog_data[
        windog_data_headers_dict["temperature"]].replace(
        -999999, np.NaN)
    windog_data[windog_data_headers_dict["speed"]] = windog_data[windog_data_headers_dict["speed"]].replace(
        -999999, np.NaN)

    return windog_data, windog_data_headers_dict


def import_windfarmer(windfarmer_filepath):
    # importing and manipulating windfarmer data into usable format
    windfarmer_dataset = pd.read_csv(windfarmer_filepath, sep='\t', header=9)
    windfarmer_dataset = windfarmer_dataset.set_index("Unnamed: 0")
    return windfarmer_dataset