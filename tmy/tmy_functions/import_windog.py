import pandas as pd
import os

def main():

    windog_data_headers_dict = {}

    # Search for txt file in inputs folder for importing
    for file in os.listdir(f"tmy/inputs"):
        if file.endswith(".txt"):
            windog_tmy_filepath = f"tmy/inputs/{file}"
        else:
            raise Exception("Missing TMY and Standard File for processing")

    # importing windog data
    windog_data = pd.read_csv(windog_tmy_filepath, sep='\t')
    # convert first column to datetime
    windog_data["Timestamp"] = pd.to_datetime(windog_data["Timestamp"], format="%m-%d-%Y %H:%M") #Changed this from the standard historical time series, need to establish a consistent formatted output
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

if __name__ == "__main__":
    main()