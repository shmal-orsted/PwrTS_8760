import pandas as pd

def main(pwts, losses_dict):
    # Get a number to apply for all losses, this can change based on additional losses added in later
    print(losses_dict)
    losses_df = pd.DataFrame.from_dict(losses_dict, orient='index', columns=['loss'])

    # multiply each value together
    total_loss = 1
    for index, value in losses_df.iterrows():
        total_loss = total_loss * float(value[0])

    # Apply losses to each timestep in the pwts
    pwts['Power'] = pwts['Power'].apply(lambda x: x*total_loss)

    # return pwts with losses applied
    return pwts

if __name__ == "__main__":
    main()