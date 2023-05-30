import math
import pandas as pd
import numpy as np

def main(windfarmer_sectors, windog_data, windog_data_headers, startup_params):
    """
    Producing a power time series. Getting the wind speed and direction in the historical time series against
    windfarmer data and producing a time series for the entire dataset

    Uses interpolation between the floor and ceil of speed bins for a gross power value from the power matrix
    :return: Power Time Series gross power on inputted historical time series
    """
    # determine sector to use for each row
    windog_data["Sector"] = windog_data[windog_data_headers["direction"]].apply(lambda x: decide_sector(x))

    # instead of determining a speed bin, going to determine which speed bins it is between, then use a ratio to determine power output
    windog_data["Gross Power"] = windog_data.apply(
        lambda x: determine_power(x[windog_data_headers["speed"]], x["Sector"],
                                  windfarmer_sectors, startup_params["farm_size"]), axis=1)

    # Bonus Feature, if there are any NaN's in the dataset return a value indicating this is a historical power time series instead of a 8760 (could also choose by len eventually)
    #is_8760 = not windog_data[windog_data_headers["direction"]].isna().any() and len(windog_data.index) == 8760
    is_8760 = startup_params["run_8760"]
    #Don't include this line if running 8760
    if is_8760:
        pass
    else:
        windog_data = windog_data.resample("1H", on=windog_data_headers["timestamp"]).mean()
    return windog_data, is_8760


def decide_sector(value):
    # determine the wind sector the direction column is in

    for x in range(0, 16):
        if pd.isna(value):
            return np.NaN
        if 11.25 + x* 22.5 <= value <= 33.75 + x*22.5:
                sector = x + 2
                return sector
        elif x == 1:
            if 360 >= value >= 348.75 or 0 <= value <= 11.25:
                sector = x + 2
                return sector


def determine_speed_bin(value):
    # rounding unless there is a nan
    if pd.isna(value):
        return np.NaN
    else:
        return round(value)


def determine_power(speed, direction, windfarmer_sectors, farm_size):

    if pd.isna(direction) or pd.isna(speed):
        return np.NaN
    else:
        # first, determine the ratio of the speed value
        ratio_value = (speed - math.floor(speed))

        # get the upper and lower values of energy production
        if speed < 0:
            speed = 0
        power_lower = windfarmer_sectors[f"Sector {int(direction)}"][math.floor(speed)]
        power_upper = windfarmer_sectors[f"Sector {int(direction)}"][math.ceil(speed)]

        if power_lower > power_upper:
            #derating scenario, when lower is higher than upper, switch them
            power_placeholder = power_lower
            power_lower = power_upper
            power_upper = power_placeholder

        # Multiply for power production above bin value
        additional_power = abs(power_upper - power_lower) * ratio_value

        # Add additional power to bin value for gross power production
        #gross_power = windfarmer_sectors[f"Sector {int(direction)}"][math.floor(speed)] + additional_power
        gross_power = power_lower + additional_power

        #value is defined in the startup_params
        if gross_power > farm_size*1000:
            return farm_size*1000
        elif gross_power < 0.1:
            return 0
        else:
            return gross_power


if __name__ == "__main__":
    main()
