import math
import pandas as pd
import numpy as np


def main(windfarmer_sectors, windfarmer_data, windog_data, windog_data_headers, startup_params, input_p50):
    """
    Producing a power time series. Getting the wind speed and direction in the historical time series against
    windfarmer data and producing a time series for the entire dataset

    Uses interpolation between the floor and ceil of speed bins for a gross power value from the power matrix
    :return: Power Time Series gross power on inputted historical time series
    """
    # todo make sure the goal seek isn't run by the power time series
    # determine sector to use for each row
    windog_data["Sector"] = windog_data[windog_data_headers["direction"]].apply(lambda x: decide_sector(x))

    is_8760 = startup_params["run_8760"]
    # Don't include this line if running 8760
    if is_8760:
        scaled_pwts = goalseek(windog_data, windfarmer_data, windog_data_headers, input_p50, windfarmer_sectors, startup_params)
        pass
    else:
        # instead of determining a speed bin, going to determine which speed bins it is between, then use a ratio to
        # determine power output
        # use the normal power time series function to get the pwts
        windog_data["Gross Power"] = windog_data.apply(
            lambda x: determine_power(x[windog_data_headers["speed"]], float(x["Sector"]), windfarmer_data,
                                      startup_params["farm_size"]), axis=1)
        windog_data = windog_data.resample("1H", on=windog_data_headers["timestamp"]).mean()
        scaled_pwts = windog_data

    # making the power time series scale to an input p50 value using a goal seek function
    # scaled_pwts = goalseek(windog_data, windfarmer_data, windog_data_headers, input_p50, windfarmer_sectors, startup_params)

    return scaled_pwts, is_8760


def goalseek(windog_data, windfarmer_data, windog_data_headers, input_p50, windfarmer_sectors, startup_params):
    """
    Goalseek function to scale p50 value to an inputted p50
    :param windog_data: a historical time series of wind data, filled or not filled, depending on 8760 status
    :param windog_data_headers: headers taken from the data file
    :param input_p50: input_p50 value given by the startup_params (to be replaced with input in interface) in GWh
    :param windfarmer_sectors: sectors from the fpm file provided from the interface
    :param startup_params: startup_params.ini provide these
    :return: scaled_pwts: scaled to the input p50 using the determine power function below
    """
    # TODO add progress bar for this into interface window using the scaling adjustment 100- value
    # changing df name for clarity
    # run use normal pwts code again to get a pwts
    # repeat while the p50 sum does not agree with the inputted p50 value
    scaling_adjustment = 0.5
    while abs(1 - scaling_adjustment) > 0.01:  # change to percentage low enough when releasing (0.01)
        # instead of determining a speed bin, going to determine which speed bins it is between, then use a ratio to
        # determine power output
        # use the normal power time series function to get the pwts
        windog_data["Gross Power"] = windog_data.apply(
            lambda x: determine_power(x[windog_data_headers["speed"]], float(x["Sector"]),
                                      windfarmer_data, startup_params["farm_size"]), axis=1)
        # compare p50 value to the inputted value and find difference
        # pwts p50 in GWh
        # get a p50 value (sum)
        pwts_p50 = windog_data["Gross Power"].sum()*0.000001
        # compare the p50 value we get out to the inputted p50
        scaling_adjustment = float(input_p50)/pwts_p50

        # scale the values in the wind speed column of the dataset to the p50
        windog_data[windog_data_headers["speed"]] = windog_data[windog_data_headers["speed"]].mul(scaling_adjustment)
        # need to get a close enough value

    scaled_pwts = windog_data

    return scaled_pwts


def decide_sector(value):
    # determine the wind sector the direction column is in

    # make the fpm file pull from 360 direction sectors
    for x in range(0, 359):
        sector = f"{round(value)}.0"
        return str(sector)


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

        # find the direction sector and value in the matrix for energy production
        try:
            power_lower = windfarmer_sectors[f"{direction}"][math.floor(speed)]
            power_upper = windfarmer_sectors[f"{direction}"][math.ceil(speed)]
        except KeyError:
            if direction == 360.0:
                direction = 0.0
            else:
                direction = direction + 0.5
            power_lower = windfarmer_sectors[f"{direction}"][math.floor(speed)]
            power_upper = windfarmer_sectors[f"{direction}"][math.ceil(speed)]

        if power_lower > power_upper:
            # derating scenario, when lower is higher than upper, switch them
            power_placeholder = power_lower
            power_lower = power_upper
            power_upper = power_placeholder

        # Multiply for power production above bin value
        additional_power = abs(power_upper - power_lower) * ratio_value

        # Add additional power to bin value for gross power production
        # gross_power = windfarmer_sectors[f"Sector {int(direction)}"][math.floor(speed)] + additional_power
        gross_power = power_lower + additional_power

        # value is defined in the startup_params
        if gross_power > farm_size * 1000:
            return farm_size * 1000
        elif gross_power < 0.1:
            return 0
        else:
            return gross_power


if __name__ == "__main__":
    main()
