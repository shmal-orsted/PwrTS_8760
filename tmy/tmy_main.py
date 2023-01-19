"""
Shawn Malone

1/18/2023

this section will be generating a tmy for an inputted historical time series if there is no input into the original
input folder. This branch will have it's own windographer data file and functions but all pwts related processes will
happen in the main branch

Inputs: MERRA2 synthesized historical time series intended to become 8760
Outputs: TMY from historical time series
"""

from tmy.tmy_functions import import_windog, tmy_process
import os


def main():

    # import .txt file in inputs
    windog_data, windog_headers = import_windog.main()
    #process data into tmy
    tmy_dataset = tmy_process.main(windog_data, windog_headers)

    #export 8760 from tmy part of project back to main branch in correct format
    return tmy_dataset


if __name__ == "__main__":
    main()
