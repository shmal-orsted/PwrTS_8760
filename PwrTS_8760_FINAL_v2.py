## 8760 Power Time Series Script
## Developed by Clay Matheny, Energy Analyst, Orsted
## Completed on May 27, 2020

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from datetime import datetime
#import datetime as dt
from datetime import datetime as dt
from pytz import timezone
from dateutil import tz


## Steps for using this tool:
#   1. Load vertically extrapolated mast data exported from Windographer. Use Datetime, Wind Speed, Wind Direction, Temperature, and Pressure. 
#   2. Load the 360 degrees sector power matrix exported from Windfarmer.
#   3. Met mast data may have different variable names project to project. Adjust below in the 'Met Mast Data' section. 
#   4. Adjust max and min temperature threshold at line 314 to turbine specific guidelines


## Load data
mydataset1 = pd.read_csv("BAD_Mast2000_8760Data.csv") # Turbine WS - Met Mast
mydataset2 = pd.read_csv("BAD_74xGE3.4MW-140_HH98m_PowerMatrix_V14.csv").iloc[:, 1:] # Power Matrix from WindFarmer


#power_matrix = mydataset2.to_numpy()
df_power_matrix = pd.DataFrame(mydataset2)


## Separate the power matrix into 12 direction sectors
bin0a = df_power_matrix.iloc[:,1:15]
bin0b = df_power_matrix.iloc[:,345:361]
bin0 = pd.concat([bin0a, bin0b], axis=1, join='inner')
bin30 = df_power_matrix.iloc[:,15:45]
bin60 = df_power_matrix.iloc[:,45:75]
bin90 = df_power_matrix.iloc[:,75:105]
bin120 = df_power_matrix.iloc[:,105:135]
bin150 = df_power_matrix.iloc[:,135:165]
bin180 = df_power_matrix.iloc[:,165:195]
bin210 = df_power_matrix.iloc[:,195:225]
bin240 = df_power_matrix.iloc[:,225:255]
bin270 = df_power_matrix.iloc[:,255:285]
bin300 = df_power_matrix.iloc[:,285:315]
bin330 = df_power_matrix.iloc[:,315:345]


bin0['Bin 0'] = bin0.mean(axis=1)
bin30['Bin 30'] = bin30.mean(axis=1)
bin60['Bin 60'] = bin60.mean(axis=1)
bin90['Bin 90'] = bin90.mean(axis=1)
bin120['Bin 120'] = bin120.mean(axis=1)
bin150['Bin 150'] = bin150.mean(axis=1)
bin180['Bin 180'] = bin180.mean(axis=1)
bin210['Bin 210'] = bin210.mean(axis=1)
bin240['Bin 240'] = bin240.mean(axis=1)
bin270['Bin 270'] = bin270.mean(axis=1)
bin300['Bin 300'] = bin300.mean(axis=1)
bin330['Bin 330'] = bin330.mean(axis=1)


power_matrix = pd.concat([bin0['Bin 0'], bin30['Bin 30'], bin60['Bin 60'], bin90['Bin 90'], 
                  bin120['Bin 120'], bin150['Bin 150'], bin180['Bin 180'], bin210['Bin 210'], 
                  bin240['Bin 240'], bin270['Bin 270'], bin300['Bin 300'], bin330['Bin 330']], axis=1, join='inner')

power_matrix = power_matrix.to_numpy()


## Met Mast Data
mast_datetime = list(mydataset1['Datetime'])
mast_ws = mydataset1['Speed_98m']   # Wind speed
mast_wd = mydataset1['dir_51m']   # Wind direction
mast_tmp = mydataset1['temp_60m'] # Temperature
mast_ps = mydataset1['pres_2m']   # Pressure


## Converts mast_datetime variable from string to datetime object (necessary to adjust time format)
dt_obj = [datetime.strptime(x,'%m/%d/%Y %H:%M') for x in mast_datetime]


## Creates hour array
hour1 = dt_obj[1].hour
hour2 = [str(i.hour) for i in dt_obj]
hour3 = [datetime.strptime(x,'%H') for x in hour2]
hour4 = [datetime.strftime(x,'%H:%M') for x in hour3]


## Creates date array
date1 = dt_obj[1].date()
date2 = [str(i.date()) for i in dt_obj]
date3 = [datetime.strptime(x,'%Y-%m-%d') for x in date2]
date4 = [datetime.strftime(x,'%m/%d/%Y') for x in date3]


### Defines initial datetime as Central and converts to UTC time
from_zone = tz.gettz('America/Central')
to_zone = tz.gettz('UTC')

dt_obj_central = [x.astimezone(from_zone) for x in dt_obj]
dt_obj_utc = [x.astimezone(to_zone) for x in dt_obj_central]


## Converts dt_obj variables back to string objects
mast_datetime = [datetime.strftime(x,'%Y-%m-%d %H:%M:%S.%f')[:-3] for x in dt_obj_utc]


## Define variables 
ws_total = mast_ws
wd_total = mast_wd
datetime = dt_obj_utc #mast9950_datetime
      
  
## Convert input data into float values
ws_total = np.array(ws_total, dtype=np.float64)
wd_total = np.array(wd_total, dtype=np.float64)


## Average monthly wind speed
ws_total_avg = np.nanmean(ws_total)


## Wind Direction Bin Function - determines which column to use in Power Matrix
def wd_bin(wind_direction):
    global j
    if wind_direction >= 345 or wind_direction < 15:
        j = 0
    elif 15 <= wind_direction < 45:
        j = 1
    elif 45 <= wind_direction < 75:
        j = 2
    elif 75 <= wind_direction < 105:
        j = 3
    elif 105 <= wind_direction < 135:
        j = 4
    elif 135 <= wind_direction < 165:
        j = 5
    elif 165 <= wind_direction < 195:
        j = 6
    elif 195 <= wind_direction < 225:
        j = 7
    elif 225 <= wind_direction < 255:
        j = 8
    elif 255 <= wind_direction < 285:
        j = 9
    elif 285 <= wind_direction < 315:
        j = 10
    elif 315 <= wind_direction < 345:
        j = 11
        
    return j

j_array = []   
for i in range(0,len(wd_total)):
    building_array = wd_bin(wd_total[i])
    j_array.append(building_array)


## Power Curve Function
def power_curve(wind_speed, j, power_matrix):

    if wind_speed < 3.0:
        turbine_speed_low, turbine_speed_up = 0.0, 3.0
        power_low, power_up = 0.0, 0.0
    elif wind_speed >= 3.0 and wind_speed < 4.0:
        turbine_speed_low, turbine_speed_up  = 3.0, 4.0
        power_low, power_up = power_matrix[3,j], power_matrix[4,j]
    elif wind_speed >= 4.0 and wind_speed < 5.0:
        turbine_speed_low, turbine_speed_up  = 4.0, 5.0
        power_low, power_up = power_matrix[4,j], power_matrix[5,j]
    elif wind_speed >= 5.0 and wind_speed < 6.0:
        turbine_speed_low, turbine_speed_up  = 5.0, 6.0
        power_low, power_up = power_matrix[5,j], power_matrix[6,j]
    elif wind_speed >= 6.0 and wind_speed < 7.0:
        turbine_speed_low, turbine_speed_up  = 6.0, 7.0
        power_low, power_up = power_matrix[6,j], power_matrix[7,j]
    elif wind_speed >= 7.0 and wind_speed < 8.0:
        turbine_speed_low, turbine_speed_up  = 7.0, 8.0
        power_low, power_up = power_matrix[7,j], power_matrix[8,j]
    elif wind_speed >= 8.0 and wind_speed < 9.0:
        turbine_speed_low, turbine_speed_up  = 8.0, 9.0
        power_low, power_up = power_matrix[8,j], power_matrix[9,j]
    elif wind_speed >= 9.0 and wind_speed < 10.0:
        turbine_speed_low, turbine_speed_up  = 9.0, 10.0
        power_low, power_up = power_matrix[9,j], power_matrix[10,j]
    elif wind_speed >= 10.0 and wind_speed < 11.0:
        turbine_speed_low, turbine_speed_up  = 10.0, 11.0
        power_low, power_up = power_matrix[10,j], power_matrix[11,j]
    elif wind_speed >= 11.0 and wind_speed < 12.0:
        turbine_speed_low, turbine_speed_up  = 11.0, 12.0
        power_low, power_up = power_matrix[11,j], power_matrix[12,j]
    elif wind_speed >= 12.0 and wind_speed < 13.0:
        turbine_speed_low, turbine_speed_up  = 12.0, 13.0
        power_low, power_up = power_matrix[12,j], power_matrix[13,j]
    elif wind_speed >= 13.0 and wind_speed < 14.0:
        turbine_speed_low, turbine_speed_up  = 13.0, 14.0
        power_low, power_up = power_matrix[13,j], power_matrix[14,j]
    elif wind_speed >= 14.0 and wind_speed < 15.0:
        turbine_speed_low, turbine_speed_up  = 14.0, 15.0
        power_low, power_up = power_matrix[14,j], power_matrix[15,j]
    elif wind_speed >= 15.0 and wind_speed < 16.0:
        turbine_speed_low, turbine_speed_up  = 15.0, 16.0
        power_low, power_up = power_matrix[15,j], power_matrix[16,j]
    elif wind_speed >= 16.0 and wind_speed < 17.0:
        turbine_speed_low, turbine_speed_up  = 16.0, 17.0
        power_low, power_up = power_matrix[16,j], power_matrix[17,j]
    elif wind_speed >= 17.0 and wind_speed < 18.0:
        turbine_speed_low, turbine_speed_up  = 17.0, 18.0
        power_low, power_up = power_matrix[17,j], power_matrix[18,j]
    elif wind_speed >= 18.0 and wind_speed < 19.0:
        turbine_speed_low, turbine_speed_up  = 18.0, 19.0
        power_low, power_up = power_matrix[18,j], power_matrix[19,j]
    elif wind_speed >= 19.0 and wind_speed < 20.0:
        turbine_speed_low, turbine_speed_up  = 19.0, 20.0
        power_low, power_up = power_matrix[19,j], power_matrix[20,j]
    elif wind_speed >= 20.0 and wind_speed < 21.0:
        turbine_speed_low, turbine_speed_up = 20.0, 21.0
        power_low, power_up = power_matrix[20,j], power_matrix[21,j]
    elif wind_speed >= 21.0 and wind_speed < 22.0:
        turbine_speed_low, turbine_speed_up = 21.0, 22.0
        power_low, power_up = power_matrix[21,j], power_matrix[22,j]
    elif wind_speed >= 22.0 and wind_speed < 23.0:
        turbine_speed_low, turbine_speed_up = 22.0, 23.0
        power_low, power_up = power_matrix[22,j], power_matrix[23,j]
    elif wind_speed >= 23.0 and wind_speed < 24.0:
        turbine_speed_low, turbine_speed_up = 23.0, 24.0
        power_low, power_up = power_matrix[23,j], power_matrix[24,j]
    elif wind_speed >= 24.0 and wind_speed < 25.0:
        turbine_speed_low, turbine_speed_up = 24.0, 25.0
        power_low, power_up = power_matrix[24,j], power_matrix[25,j]
    elif wind_speed >= 25.0 and wind_speed < 26.0:
        turbine_speed_low, turbine_speed_up = 25.0, 26.0
        power_low, power_up = power_matrix[25,j], power_matrix[26,j]
    elif wind_speed >= 26.0 and wind_speed < 27.0:
        turbine_speed_low, turbine_speed_up = 26.0, 27.0
        power_low, power_up = power_matrix[26,j], power_matrix[27,j]
    elif wind_speed >= 27.0 and wind_speed < 28.0:
        turbine_speed_low, turbine_speed_up = 27.0, 28.0
        power_low, power_up = power_matrix[27,j], power_matrix[28,j]
    elif wind_speed >= 28.0 and wind_speed < 29.0:
        turbine_speed_low, turbine_speed_up = 28.0, 29.0
        power_low, power_up = power_matrix[28,j], power_matrix[29,j]
    elif wind_speed >= 29.0 and wind_speed < 30.0:
        turbine_speed_low, turbine_speed_up = 29.0, 30.0
        power_low, power_up = power_matrix[29,j], power_matrix[30,j]
    elif wind_speed >= 30.0 and wind_speed < 31.0:
        turbine_speed_low, turbine_speed_up = 30.0, 31.0
        power_low, power_up = power_matrix[30,j], power_matrix[31,j]
    elif wind_speed >= 31.0 and wind_speed < 32.0:
        turbine_speed_low, turbine_speed_up = 31.0, 32.0
        power_low, power_up = power_matrix[31,j], power_matrix[32,j]
      
    return turbine_speed_low,turbine_speed_up, power_low, power_up, wind_speed # 


## Power Curve Derived Generation Function
def pcdg_calc(ws_input,j,power_matrix,power_curve):
    pcdg_input = []   
    for i in range(0,len(ws_input)):
        if math.isnan(ws_input[i]):
            pcdg_i = float('nan')
        elif ws_input[i] < 33.0:
            turbine_speed_low,turbine_speed_up,power_low,power_up,wind_speed = power_curve(ws_input[i],j[i],power_matrix)
            pcdg_i = ((power_low + (power_up - power_low) * ((wind_speed-turbine_speed_low) / (turbine_speed_up-turbine_speed_low)))) / 1000     # [MWh]
        elif ws_input[i] >= 33.0:
            pcdg_i = 0.0
        pcdg_input.append(pcdg_i) 
        
    return pcdg_input


## Call PCDG function
pcdg_total = pcdg_calc(ws_total,j_array,power_matrix,power_curve)


## Convert PCDG to float values
pcdg_total = np.array(pcdg_total, dtype=np.float64)


## Round pcdg_total to one decimal place
pcdg_total_round = [round(i,1) for i in pcdg_total]
pcdg_total_round = np.array(pcdg_total_round, dtype=np.float64)


## Calculate the sum of the PCDG
pcdg_sum_total = np.nansum(pcdg_total)


## Calculate air density
r = 287.058                                # Gas constant 
mast_tmpK = [i + 273.15 for i in mast_tmp] # Convert to Kelvin
mast_ps = [i * 100 for i in mast_ps]       # Convert from mbar to Pa
mast_den = [mast_ps[i] / (r * mast_tmpK[i]) for i in range(len(mast_ws))]
print('den min = ', np.nanmin(mast_den))
print('den max = ', np.nanmax(mast_den))


## Converts datetime from UTC to Central and then removes timezone info
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/Central')

datetime_utc = [x.astimezone(from_zone) for x in datetime]
datetime_central = [x.astimezone(to_zone) for x in datetime_utc]
datetime = [x.replace(tzinfo=None) for x in datetime_central]


## Create a dataframe for the final power output
df_pwrTS = np.column_stack((datetime, mast_ws, mast_wd, mast_tmp, pcdg_total_round))
df_pwrTS = pd.DataFrame(df_pwrTS, columns=['Datetime', 'Wind Speed [m/s]', 'Wind Direction [Degrees]', 'Temp [C]', 'Gross Power [MWh]'])
df_pwrTS = df_pwrTS.set_index('Datetime')


## Delete power data when temp is greater than 40 C or below 0 C
df_pwrTS['Power (Temp Adj)'] = [df_pwrTS['Gross Power [MWh]'][i]*0.0 if df_pwrTS['Temp [C]'][i] > 40 else df_pwrTS['Gross Power [MWh]'][i]*1 for i in range(len(df_pwrTS['Gross Power [MWh]']))]
df_pwrTS['Power (Temp Adj)'] = [df_pwrTS['Gross Power [MWh]'][i]*0.0 if df_pwrTS['Temp [C]'][i] < 0 else df_pwrTS['Gross Power [MWh]'][i]*1 for i in range(len(df_pwrTS['Gross Power [MWh]']))]


## Make a 2% downward adjustment to power output due to electrical losses                   
df_pwrTS['Net Power [MWh]'] = [i * 0.98 for i in df_pwrTS['Power (Temp Adj)']] # loss of 2%




## Convert missing data (i.e. 9999) to NaN values
df_pwrTS[df_pwrTS == 9999] = np.nan


## Final power dataframe 
df_pwrTS_FINAL = df_pwrTS[["Wind Speed [m/s]", "Wind Direction [Degrees]", 'Temp [C]', 'Gross Power [MWh]', 'Net Power [MWh]']].copy()
df_pwrTS_FINAL.to_csv('BAD_8760_nanTest_2021.11.05.csv', index=True)





