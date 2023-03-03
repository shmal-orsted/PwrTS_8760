import pandas as pd
import os
import datetime
import math


def export_csv(pwts, working_dir, is_8760):
    # Make path to export to, incorporating if it is an 8760
    cwd = os.getcwd()
    if is_8760:
        filename = f"8760 - {datetime.datetime.date(datetime.datetime.now())}"
    else:
        filename = f"Power Time Series - {datetime.datetime.date(datetime.datetime.now())}"

    path = f"exports/{filename}.csv"
    #Divide pwts columns into MWh
    pwts["Gross Power (MWh)"] = pwts["Gross Power"]/1000
    pwts["Net Power (MWh)"] = pwts["Net Power"] / 1000
    pwts = pwts.drop(["Gross Power", "Net Power"], axis=1)
    pwts.to_csv(path)
    return


def peer_review_print(is_8760, total_loss, sum_power, losses_sum):
    timestamp = datetime.datetime.now()

    with open("exports/review.txt", "a") as f:
        f.write("\n")
        f.write(f"\n{timestamp}\n")
        f.write("Power Time Series Run with Parameters:\n")
        f.write(f"8760 = {is_8760}\n")
        f.write(f"Total Loss Applied = {total_loss}\n")
        f.write(f"Gross Power (GWh) = {math.floor(sum_power/1000000)}\n")
        f.write(f"Net Power (GWh) = {math.floor(losses_sum/1000000)}")
    return
