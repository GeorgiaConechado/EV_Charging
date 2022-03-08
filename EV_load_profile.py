import datetime as dt
from doctest import Example
import numpy as np
import pandas as pd

EV_inputs_example = { #EV model details example
    'AC_charge_rate':11, #max charge rate kW
    'DC_charge_rate':100, #max charge rate kW
    'battery_size': 75, #kWh - this not being used atm
}

traffic_inputs_2020 = {
    'year': 2030, # the year for analysis
    'traffic_mu': 28,  #forecast mean daily EV traffic volume (two way)
    'traffic_sigma':5, #standard deviation for the traffic volume
    'stop_prob':0.2, #probability of car passing by to stop
    'hourly_weight':[2,2,1,1,1,1,3,7,14,20,23,27,26,25,23,17,13,8,5,3,3,2,2,2], #rough weightings for probability of EV arriving at each time of day
}

"""
Determining the EV arrival times from the traffic data is done in three steps:
1. Variation of daily traffic volume from given mean traffic, using normal distribution
2. Probability each EV will stop
3. Generate arrival time for each of these EVs, using manually input probability weightings from given hourly profile
(If not using a given hourly profile could make this normal distribution instead)
"""

def load_profile(EV_inputs, traffic_inputs): #generates timeseries csv
    times = [(dt.time(i).strftime('%H:%S')) for i in range(24)]
    init_date = dt.date(traffic_inputs['year'],1,1)
    day = dt.timedelta(days = 1)
    dates = [((init_date + i*day).strftime('%d/%m/%Y')) for i in range(365)]

    load = []    
    for i in range (365):
        daily_load = []
        arrival_times = randomise_travel(traffic_inputs)
        for j in range (24):
            daily_load.append(EV_inputs['DC_charge_rate']*np.count_nonzero(arrival_times == j))
        load.append(daily_load)

    df = pd.DataFrame(load, index = dates, columns = times)
    df.to_csv('timeseries/' + str(traffic_inputs['year']) + '_EV_load_profile')
    return    

def randomise_travel(traffic_inputs): #simplest version - random times of day
    traffic = np.round(np.random.normal(loc= traffic_inputs['traffic_mu'], scale = traffic_inputs['traffic_sigma']))
    arrival_times = np.random.choice(24,size=int(traffic*traffic_inputs['stop_prob']),p=probability(traffic_inputs['hourly_weight']))
    return arrival_times

def probability(weightings):
    total = sum(weightings)
    p = []
    for i in range(len(weightings)):
        p.append(weightings[i]/total)
    return p

load_profile(EV_inputs_example,traffic_inputs_2020)
