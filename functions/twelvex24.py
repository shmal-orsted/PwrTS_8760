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
    pwts_hm = pwts.groupby(['Month', "Hour"]).mean()

    # add to 12x24 dataframe in format
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    twelvex24_var = pd.DataFrame(columns=[month_list])

    # Generate 12x24 from dataframe
    for x in range(0, 12):
        series_to_add = pwts_hm["Net Power"][x*24:x*24+24]
        series_to_add = series_to_add.reset_index()["Net Power"]
        twelvex24_var[month_list[x]] = series_to_add

    # Convert Dataframe of 12x24 to percentage of 8760
    pwts_sum = pwts["Net Power"].sum()
    percent_twelvex24 = (twelvex24_var/pwts_sum)*100


    # making the tmy_dataset into a functional one matching formatting of rest of code
    pwts = pwts.reset_index()

    return percent_twelvex24, twelvex24_var, pwts

if __name__ == "__main__":
    main()


