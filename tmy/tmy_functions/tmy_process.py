"""
Processing a timestep windographer dataset that has been synthesized with MERRA2 data to fill in any gaps in data
into a TMY (Typical Meteorological Year) by taking the most representative month averaged across the entire timeseries
and repeating for each month

inputs: windographer dataframe, windographer dataframe headers
outputs: tmy
"""

import pandas as pd
from datetime import datetime


def main(windog_df, windog_headers):
    # resample dataset to hourly
    windog_df = windog_df.resample("1H", on=windog_headers["timestamp"]).mean()

    # Average all years and separate out months
    #Creating month and year columns
    windog_df["Month"] = windog_df.index
    windog_df["Month"] = windog_df["Month"].apply(lambda x: x.month)
    windog_df["Year"] = windog_df.index
    windog_df["Year"] = windog_df["Year"].apply(lambda x: x.year)

    # overall monthly means shortened variable name
    omm = windog_df.groupby('Month').mean()
    # Individual year means shortened variable name
    iym = windog_df.groupby(['Month', 'Year']).mean()

    # select representative from iym closest to value in omm
    # need months and years columns to get the values I need from each year
    iym["Month"] = iym.index
    iym["Month"] = iym["Month"].apply(lambda x: x[0])

    tmy_list = []
    # Loop through each month
    for x in range(1, 13):
        dataset_average = omm[windog_headers['speed']][x]
        # get value closest to what we are looking for of each month
        iym_sort = pd.DataFrame(
            iym[iym["Month"] == x][windog_headers["speed"]].apply(lambda x: x - dataset_average).abs().sort_values())
        # Get the year from that index and add to a dictionary/list for tmy
        iym_sort["Year"] = iym_sort.index
        iym_sort["Year"] = iym_sort["Year"].apply(lambda y: y[1])
        tmy_list.append((x, iym_sort["Year"].iloc[0]))

    # for each month, select the representative month from the time series and add to tmy
    # use conditions to choose the month from the dataset to use in the TMY
    # using tmy_list loop through the tuples and get the corresponding month from the year listed and create a tmy
    tmy_dataset = pd.DataFrame()
    for date_tuple in tmy_list:
        tmy_dataset = pd.concat([tmy_dataset, (windog_df.loc[(windog_df["Month"] == date_tuple[0]) & (windog_df["Year"]
                                                                                                      == date_tuple[
                                                                                                          1])])])

    return tmy_dataset


if __name__ == "__main__":
    main()
