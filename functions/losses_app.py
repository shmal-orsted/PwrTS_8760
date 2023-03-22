import pandas as pd

def main(pwts, losses_dict, headers, startup_params):
    # Get a number to apply for all losses, this can change based on additional losses added in later
    losses_df = pd.DataFrame.from_dict(losses_dict, orient='index', columns=['loss'])

    # for review get total energy production pre-losses
    sum_power = pwts["Gross Power"].sum()
    # multiply each value together
    total_loss = 1
    for index, value in losses_df.iterrows():
        total_loss = total_loss * float(value[0])

    # temporary addition of a temperature shutdown to get this out the door. Will be replaced with temperature derating calculation later
    low_temp = startup_params["low_temp"]
    high_temp = startup_params["high_temp"]

    pwts['Gross Power'] = pwts.apply(lambda x: temp_shutdown(low_temp, high_temp, x[headers["temperature"]], x["Gross Power"]), axis=1)

    # Apply losses to each timestep in the pwts
    pwts['Net Power'] = pwts['Gross Power'].apply(lambda x: x*total_loss)

    # for review, get losses total power generated
    losses_sum = pwts['Net Power'].sum()

    # return pwts with losses applied
    return pwts, total_loss, sum_power, losses_sum

def temp_shutdown(low, high, temp, power):
    if temp < low:
        return 0
    elif temp > high:
        return 0
    else:
        return power

if __name__ == "__main__":
    main()