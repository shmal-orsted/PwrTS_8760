import os.path

import numpy as np
import pandas as pd
import math


def main(pwts, losses_dict, headers, startup_params, working_dir):
    # Get a number to apply for all losses, this can change based on additional losses added in later
    losses_df = pd.DataFrame.from_dict(losses_dict, orient='index', columns=['loss'])

    # multiply each value together
    bulk_loss = 1
    for index, value in losses_df.iterrows():
        bulk_loss = bulk_loss * float(value[0])

    #apply temperature shutdown to the time series and gather the value of that loss first
    pwts = temp_shutdown(pwts=pwts, low=startup_params["low_temp"], high=startup_params["high_temp"], headers=headers)

    # import derating curve from data file
    derating_curve = import_derating_curve(startup_params["turbine_model"], startup_params["derating_altitude"], working_dir)

    #multiply derating curve by number of turbines to get farm derating curve
    derating_curve["Power (kW)"] = derating_curve["Power (kW)"]*int(startup_params["num_turbines"])

    # derating loss will be added to time series here
    pwts['Gross Power + Derating'] = pwts.apply(
        lambda x: temp_derating(x["Gross Power"], x[headers['temperature']], derating_curve), axis=1)

    # Getting values out of aggregate value from derating function
    pwts["Temperature Derating Loss Value (kW)"] = pwts.apply(lambda x: x["Gross Power + Derating"][1], axis=1)
    pwts['Gross Power'] = pwts.apply(lambda x: x["Gross Power + Derating"][0], axis=1)

    # add consumption losses based on manufacturer specs
    # TODO replace this with a param pulled from the derating curve document
    pwts["Consumption Loss Value"] = pwts[headers['temperature']].apply(lambda x: 21 if x <= 5 else 0)

    # Apply bulk losses to each timestep in the pwts
    # speed testing 9.01 ms ± 351 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
    # pwts['Net Power'] = pwts['Gross Power'].apply(lambda x: x * total_loss)
    # speed testing 128 µs ± 1.5 µs per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
    pwts['Net Power'] = pwts['Gross Power']*bulk_loss

    # Apply consumption loss to each timestep in the pwts
    pwts['Net Power'] = pwts['Net Power']-pwts["Consumption Loss Value"]

    # Grid Curtailment - Applied last to the net pwts
    pwts['Net Power + Curtailment Loss'] = pwts.apply(lambda x: grid_curtailment(x["Net Power"], float(startup_params["grid_curtailment_limit"])*1000), axis=1)

    # Split grid curtailment tuple
    pwts['Net Power'] = pwts.apply(lambda x: x["Net Power + Curtailment Loss"][0], axis=1)
    pwts['Curtailment Loss'] = pwts.apply(lambda x: x["Net Power + Curtailment Loss"][1], axis=1)

    # return pwts with losses applied
    return pwts, bulk_loss


def temp_shutdown(pwts, low, high, headers):
    """
    Meant to create a column for lost power due to turbine shutdown. Every value in the gross power column that occurs
    outside of the defined temperature limits in the startup params is cut to 0, the loss is tallied and returned
    input
    pwts: power time series without losses applied
    low: low temp for temp shutdown to apply
    high: high temp for temp shutdown to apply
    outputs
    pwts: pwts with a power column that includes the temp shutdown applied and a column with temp shutdown applied
    total_loss: total shutdown loss from the function
    """

    pwts["Temp Shutdown Loss"] = pwts.apply(lambda x:
                                                    x["Gross Power"] if low > x[headers['temperature']] > high else 0, axis=1)

    return pwts


def temp_derating(power, temp, turbine_derating_curve):
    """
    temperature derating:
    input
    power: power produced from the pwts function
    temp: Determining power derating based on temperature
    turbine_derating_curve: based on input from pre-defined values
    output
    derated_power: power reduced based on the input:power, derating curve and temperature
    power_lost: lost power to temp derating to be added to a final count and a loss factor to be generated
    """

    # num_turbines = int(num_turbines)

    # get max power for derating curve on whole farm
    # turbine_derating_curve["Power (kW)"] = turbine_derating_curve["Power (kW)"]*num_turbines

    # find power cap with interpolation
    # floor and ceiling temp value to determine interpolation values
    try:
        temp_round_down = math.floor(temp)
        temp_round_up = math.ceil(temp)
    except ValueError:
        derated_power = np.NaN
        power_loss = np.NaN
        return derated_power, power_loss

    # check for issues with high or low temperature
    if temp_round_down < -30:
        temp_round_down = -30
    if temp_round_up < -30:
        temp_round_up = -30
    if temp_round_up > 50:
        temp_round_up = 50

    # determine power value limit
    try:
        lower_value = turbine_derating_curve[turbine_derating_curve["Temp (C)"] == temp_round_down]["Power (kW)"].values[0]
        upper_value = turbine_derating_curve[turbine_derating_curve["Temp (C)"] == temp_round_up]["Power (kW)"].values[0]
    except IndexError:
        if power == np.nan:
            return np.nan

    if 30 < temp < 33:
        # interpolate for power limit
        temp_diff = temp - temp_round_down
        power_cap = lower_value - (temp_diff*(upper_value - lower_value))
        if power_cap < power:
            derated_power = power_cap
            power_loss = power - power_cap
        else:
            derated_power = power
            power_loss = 0.0
    else:
        derated_power = power
        power_loss = 0.0

    return derated_power, power_loss


def import_derating_curve(turbine_model, altitude, working_dir):
    """
    import derating curve from turbine data library and choose the appropriate derating curve based on the input elevation
    inputs
    turbine_model: input from the startup_params file - currently supported turbines (ge34)
    altitude: input from the startup_params file - must appear on the derating curve from the manufacturer. Check the
    derating files for accepted altitudes per turbine
    working_dir: working project directory, used in selecting the turbine derating curve filepath
    outputs
    derating_curve: the derating curve for the turbine and altitude selected in the params file
    """
    # import data file
    filepath = os.path.join(working_dir, "derating_curves", f"{turbine_model}_derating_curve.csv")
    derating_curve_all_alts = pd.read_csv(filepath)

    # select appropriate data using altitude param
    derating_curve = derating_curve_all_alts[["Temperature", f"Power ({altitude}m)"]]

    # rename column headers
    derating_curve = derating_curve.rename(columns = {"Temperature": "Temp (C)", f"Power ({altitude}m)": "Power (kW)"})

    return derating_curve


def grid_curtailment(net_power, grid_cap):
    """
    limit and sum the excess energy produced from the system to a limited grid cap provided
    inputs
    net_power: value of power generated, derated and losses applied before grid curtailing
    grid_cap: input from the startup_params file used to find the loss here
    outputs
    net_power_curtailed: net power curtailed and limited to the grid cap
    curtailment_amount: value of energy over the curtailment limit to be summed for a loss
    """
    if net_power > grid_cap:
        curtailment_amount = net_power - grid_cap
        net_power = grid_cap
        return net_power, curtailment_amount
    else:
        curtailment_amount = 0
        return net_power, curtailment_amount


if __name__ == "__main__":
    main()
