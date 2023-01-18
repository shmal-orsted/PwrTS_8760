import pandas as pd

def main(pwts, losses_dict):
    # Get a number to apply for all losses, this can change based on additional losses added in later
    losses_df = pd.DataFrame.from_dict(losses_dict, orient='index', columns=['loss'])

    # for review get total energy production pre-losses
    sum_power = pwts["Power"].sum()
    # multiply each value together
    total_loss = 1
    for index, value in losses_df.iterrows():
        total_loss = total_loss * float(value[0])

    # Apply losses to each timestep in the pwts
    pwts['Power'] = pwts['Power'].apply(lambda x: x*total_loss)
    # for review, get losses total power generated
    losses_sum = pwts['Power'].sum()

    # return pwts with losses applied
    return pwts, total_loss, sum_power, losses_sum

if __name__ == "__main__":
    main()