import pandas as pd
import numpy as np

def main(windfarmer_sectors, windog_data, windog_data_headers):
    """
    Producing a power time series. Getting the wind speed and direction in the historical time series against
    windfarmer data and producing a time series for the entire dataset

    Does not use iterrows, much faster this way
    :return: Power Time Series
    """

    # determine sector to use for each row
    windog_data["Dir Sector"] = windog_data[windog_data_headers["direction"]].apply(lambda x: decide_sector(x))

    # use direction sector and wind speed to get power production at that time stamp in the correct direction sector
    windog_data["Speed Bin"] = windog_data[windog_data_headers["speed"]].apply(lambda speed: determine_speed_bin(speed))

    # use determined speed bin, direction sector to get power from windfarmer data for each row
    windog_data["Power"] = windog_data.apply(lambda x: determine_power(x["Dir Sector"], x["Speed Bin"], windfarmer_sectors), axis=1)

    # Bonus Feature, if there are any NaN's in the dataset return a value indicating this is a historical power time series instead of a 8760 (could also choose by len eventually)
    is_8760 = windog_data[windog_data_headers["direction"]].isna().any()

    return windog_data, is_8760


def decide_sector(value):
    # determine the wind sector the direction column is in

    for x in range(0, 16):
        if pd.isna(value):
            return np.NaN
        if 11.25 + x* 22.5 < value < 33.75 + x*22.5:
                sector = x + 2
                return sector
        elif x == 1:
            if 360 >= value > 348.75 or 0 < value < 11.25:
                sector = x + 2
                return sector


def determine_speed_bin(value):
    # rounding unless there is a nan
    if pd.isna(value):
        return np.NaN
    else:
        return round(value)


def determine_power(direction_sector, speed_bin, windfarmer_sectors):
    # determine the power number for each direction sector/speed row
    if pd.isna(direction_sector):
        return np.NaN
    else:
        return windfarmer_sectors[f"Sector {int(direction_sector)}"][speed_bin]


if __name__ == "__main__":
    main()