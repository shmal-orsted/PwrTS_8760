import pandas as pd


def main(windfarmer_data):
    # This should be removed if we decide to use individual direction degrees for 8760s
    # split direction sectors into new columns and a new dataframe
    list_of_dfs = []

    # getting steps from 0-359 in 16 steps
    # low = 348.75
    # high = 11.25
    # sector = 1

    # need to round the numbers to index them

    # if low > 359:
    #     low = low - 360

    # if high > 359:
    #     pass


    for x in range(0, 16, 1):

        low = 348.75 + x*22.5
        high = 11.25 + x*22.5

        if low > 359:
            low = low - 360

        if low > high:
            temp_df = pd.DataFrame(windfarmer_data.loc[:, str(float(round(low))):(str(359.0))]).join(
                windfarmer_data.loc[:, str(0.0):str(float(round(high)))])
            list_of_dfs.append(temp_df)
        else:
            list_of_dfs.append(pd.DataFrame(windfarmer_data.loc[:, str(float(round(low))):str(float(round(high)))]))

    # this is a list of all the sectors
    print(list_of_dfs)

    # define a sectors df
    sectors = pd.DataFrame()

    sector_label = 1
    # Average and combine the sectors
    for df in list_of_dfs:
        # Make this add the new mean'd column to the sectors df
        # sectors.join(df.mean(axis=1).to_frame())
        # sector_label += 1

        # Give it another try
        sectors[f"Sector {sector_label}"] = df.mean(axis=1)
        sector_label += 1


    # Sectors should be a dataframe with each column a mean sector from above
    return sectors


if __name__ == "__main__":
    main()
