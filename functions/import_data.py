import pandas as pd
from tmy import tmy_main

def import_windog(windog_filepath):

    windog_data_headers_dict = {}

    # TMY will engage here if there is no windog file (.txt) in inputs directory
    if windog_filepath is None:
        print("Missing Windog File, Defaulting to TMY")
        windog_data = tmy_main.main()
    else:
        # importing windog data
        windog_data = pd.read_csv(windog_filepath, sep='\t', header=10)
        # convert first column to datetime
        windog_data["Timestamp"] = pd.to_datetime(windog_data["Timestamp"], format="%m-%d-%Y %H:%M")

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