import pandas as pd
import os
import datetime
import math


def export_csv(pwts, working_dir, is_8760):
    # Make path to export to, incorporating if it is an 8760
    cwd = os.getcwd()
    if is_8760:
        filename = f"8760 - {datetime.datetime.date(datetime.datetime.now())}_{datetime.datetime.time(datetime.datetime.now()).strftime('%H_%M')}"
    else:
        filename = f"Power Time Series - {datetime.datetime.date(datetime.datetime.now())}_{datetime.datetime.time(datetime.datetime.now()).strftime('%H_%M')}"

    path = os.path.join(working_dir, "exports", f"{filename}.csv")
    #Divide pwts columns into MWh
    pwts["Gross Power (MWh)"] = round(pwts["Gross Power"]/1000, 2)
    pwts["Net Power (MWh)"] = round(pwts["Net Power"] / 1000, 2)
    pwts = pwts.drop(["Gross Power", "Net Power"], axis=1)

    # dropping all the columns we don't want in the output file
    pwts_output = pwts.drop(["Month", "Year", "Sector", "Temp Shutdown Loss", "Gross Power + Derating",
               "Temperature Derating Loss Value (kW)", "Consumption Loss Value",
               "Net Power + Curtailment Loss", "Curtailment Loss"], axis=1)
    pwts_output.to_csv(path)
    return


def peer_review_print(pwts, is_8760, bulk_loss, working_dir):
    timestamp = datetime.datetime.now()

    # TODO Add bulk losses to output file for review
    # calculate total losses from consumption in % and power (kW)
    if pwts["Consumption Loss Value"].sum() != 0:
        consumption_loss_percent = 100 * (pwts["Consumption Loss Value"].sum()/pwts["Gross Power"].sum())
    else:
        consumption_loss_percent = 0
    consumption_loss = pwts["Consumption Loss Value"].sum()

    # and derating in % and power
    if pwts["Temperature Derating Loss Value (kW)"].sum() != 0:
        derating_loss_percent = pwts["Temperature Derating Loss Value (kW)"].sum() / pwts["Gross Power"].sum()
    else:
        derating_loss_percent = 0
    derating_loss = pwts["Temperature Derating Loss Value (kW)"].sum()

    # and shutdown in % and power
    if pwts["Temp Shutdown Loss"].sum() != 0:
        shutdown_loss_percent = pwts["Temp Shutdown Loss"].sum() / pwts["Gross Power"].sum()
    else:
        shutdown_loss_percent = 0
    shutdown_loss = pwts["Temp Shutdown Loss"].sum()

    # and curtailment in % and power
    if pwts["Curtailment Loss"].sum() != 0:
        curtailment_loss_percent = 100 * pwts["Curtailment Loss"].sum() / pwts["Gross Power"].sum()
    else:
        curtailment_loss_percent = 0
    curtailment_loss = pwts["Curtailment Loss"].sum()

    # for review get total energy production pre-losses
    sum_power = pwts["Gross Power"].sum()

    # for review, get losses total power generated
    losses_sum = pwts['Net Power'].sum()

    with open(os.path.join(working_dir,"exports", "review.txt"), "a") as f:
        f.write("\n\n")
        f.write(f"\n{timestamp}\n")
        f.write("Power Time Series Run with Parameters:\n")
        f.write(f"8760 = {is_8760}\n")
        f.write(f"Total Bulk Loss Applied = {bulk_loss}\n")
        f.write(f"Gross Power (GWh) = {round((sum_power/1000000), 3)}\n")
        f.write(f"Net Power (GWh) = {round((losses_sum/1000000), 3)}\n")
        f.write(f"Consumption Loss Factor = {round(100 - (consumption_loss_percent*100), 3)}\n")
        # f.write(f"Consumption Loss Value (kW) = {consumption_loss)}")
        f.write(f"Derating Loss Factor = {round(100 - (derating_loss_percent*100), 3)}\n")
        # f.write(f"Derating Loss Value (kW) = {derating_loss)}")
        f.write(f"Shutdown Loss Factor = {round(100 - (shutdown_loss_percent * 100), 3)}\n")
        # f.write(f"Shutdown Loss Value (kW) = {shutdown_loss)}")
        f.write(f"Grid Curtailment Loss Factor = {round(100 - (curtailment_loss_percent * 100), 3)}\n")
        # f.write(f"Shutdown Loss Value (kW) = {curtailment_loss)}")
    return
