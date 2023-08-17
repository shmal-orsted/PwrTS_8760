import pandas as pd

def main(pwts):
    """
    Sorting and averaging the time series by month and hour, then averaging, adding to a 12x24 output

    :param pwts:
    pwts - processed pwts coming from the main part of the code. This will only trigger if it's running an 8760
    :return:
    twelvex24_var - 12x24 from the input 8760
    """
    pwts

    # set index to the timestamp column
    pwts = pwts.set_index("Timestamp")
    # add hour column into dataframe
    pwts["Hour"] = pwts.index
    pwts["Hour"] = pwts["Hour"].apply(lambda x: x.hour)
    # sort by hour and month into a dataframe
    # this should be sum instead of mean? depending on what is being requested
    pwts_hm = pwts.groupby(['Month', "Hour"]).sum()

    # add to 12x24 dataframe in format
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    twelvex24_var_net = pd.DataFrame(columns=[month_list])

    # Gross Power and Net Power
    # Generate 12x24 from dataframe
    for x in range(0, 12):
        series_to_add = pwts_hm["Net Power"][x*24:x*24+24]
        series_to_add = series_to_add.reset_index()["Net Power"]
        twelvex24_var_net[month_list[x]] = series_to_add

    # Convert Dataframe of 12x24 to percentage of 8760
    pwts_sum = pwts["Net Power"].sum()
    percent_twelvex24_net = (twelvex24_var_net/pwts_sum)*100

    # Convert Dataframe of 12x24 to percentage of 8760
    pwts_sum = pwts["Net Power"].sum()
    percent_twelvex24_net = (twelvex24_var_net / pwts_sum) * 100

    # add to 12x24 dataframe in format
    twelvex24_var_gross = pd.DataFrame(columns=[month_list])

    # Generate 12x24 from dataframe
    for x in range(0, 12):
        series_to_add = pwts_hm["Gross Power"][x * 24:x * 24 + 24]
        series_to_add = series_to_add.reset_index()["Gross Power"]
        twelvex24_var_gross[month_list[x]] = series_to_add

    # Convert Dataframe of 12x24 to percentage of 8760
    pwts_sum = pwts["Gross Power"].sum()
    percent_twelvex24_gross = (twelvex24_var_net / pwts_sum) * 100

    # making the tmy_dataset into a functional one matching formatting of rest of code
    pwts = pwts.reset_index()

    # converting units and rounding
    twelvex24_var_net = twelvex24_var_net.mul(0.000001).round(2)
    twelvex24_var_gross = twelvex24_var_gross.mul(0.000001).round(2)


    return percent_twelvex24_net, twelvex24_var_net, percent_twelvex24_gross, twelvex24_var_gross, pwts

if __name__ == "__main__":
    main()


