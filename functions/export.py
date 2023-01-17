import pandas as pd
import os
import datetime


def export_csv(pwts, working_dir, is_8760):
    # Make path to export to, incorporating if it is an 8760
    cwd = os.getcwd()
    if is_8760:
        filename = f"8760 - {datetime.datetime.date(datetime.datetime.now())}"
    else:
        filename = f"Power Time Series - {datetime.datetime.date(datetime.datetime.now())}"

    path = f"exports/{filename}.csv"
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
        f.write(f"Sum Power (Pre-Losses) = {sum_power}\n")
        f.write(f"Sum Power (Post-Losses = {losses_sum}")
    return