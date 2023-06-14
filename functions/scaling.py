import pandas as pd
import math
import numpy as np


def main(windog_data, startup_params, headers):
    """
    Scaling wind speeds in the met data to a value given in the startup_params. The scaling will scale the mean of monthly
    means values after calculating them then apply that scaling factor to the dataset, returning a scaled dataset to be
    run in the main code afterwards.
    input
    windog_data: windographer dataset from the main code
    scaling_factor: the value to scale the time series to. Must be a float value
    output
    scaled_dataset: the scaled dataset that is output for further processing
    """

    # use below function to determine the MoMM of the dataset
    momm = momm_calc(windographer_dataset=windog_data, headers=headers)

    # use momm from function and find scaling factor for dataset comparing to scaling_value in startup_params
    scale_to_apply = float(startup_params['scaling_value'])/momm

    # scale dataset to new windspeed
    windog_data[headers['speed']] = windog_data[headers['speed']]*scale_to_apply

    return windog_data, momm


def momm_calc(windographer_dataset, headers):
    """
    Calculate the mean of monthly means of the input dataset. This can be applied to 8760 or power time series
    input
    windographer_dataset: dataframe of wind speed time series
    output
    momm: a scalar value of momm for the input dataset.
    """
    momm = 0
    # replace all -999999 values in windspeed column with nan values
    windographer_dataset[headers['speed']] = windographer_dataset[headers['speed']].replace(-999999, np.nan)

    # calculate averages of each month
    monthly_means = windographer_dataset.groupby(['Year', 'Month']).mean()
    # calculate timesteps in each month
    monthly_means['num_timesteps'] = windographer_dataset.groupby(['Year', 'Month']).size()

    # use timesteps and averages to calculate momm for entire dataset
    monthly_means["speed*size"] = monthly_means[headers['speed']]*monthly_means['num_timesteps']

    # momm value
    momm = monthly_means['speed*size'].sum()/monthly_means['num_timesteps'].sum()

    windographer_dataset
    return momm


if __name__ == "__main__":
    main()