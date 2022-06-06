import datetime as dt
from doctest import Example
from turtle import shape
import numpy as np
import pandas as pd
import scipy.stats as stats 

# hourly_weight = [2,2,1,1,1,1,3,7,14,20,23,27,26,25,23,17,13,8,5,3,3,2,2,2] #example taken from stuart highway evernergi report

def arrival_times(traffic_mu, traffic_sigma, hourly_weight, stop_prob = 1):
    '''
    Determine hourly arrival times over a year. Uses a near-ideal normal distribution for day-to-day variation, and a given distribution profile for hour-to-hour variation.
    '''
    yearly_arrival_times = []
    stdMax = 2.78
    trafficLin = np.linspace(traffic_mu -stdMax*traffic_sigma,traffic_mu+stdMax*traffic_sigma,365)
    trafficBigArray = np.random.normal(loc = traffic_mu, scale = traffic_sigma,size=1000000)
    trafficQuants = np.linspace(0.0,0.997,365)
    traffic = np.round(np.quantile(trafficBigArray,trafficQuants))
    traffic[traffic < 0] = 0
    np.random.shuffle(traffic)    
    for i in range (365):
        daily = []
        arrival_times = np.random.choice(24,size=int(traffic[i]*stop_prob),p=probability(hourly_weight))
        for j in range (24):
            daily.append(np.count_nonzero(arrival_times == j))
        yearly_arrival_times.append(daily)
    return yearly_arrival_times


def probability(weightings):
    total = sum(weightings)
    p = []
    for i in range(len(weightings)):
        p.append(weightings[i]/total)
    return p


def char_profile (yearly_arrival_times, num_chargers):
    char_profile = []
    current_wait_EV = []
    total_prev_wait_EV = []

    for i in range(len(yearly_arrival_times)):
        daily_char = []
        daily_times = yearly_arrival_times[i]
        wait_EV_record = []
        for j in range(len(daily_times)):
            arriving_EVs = daily_times[j]
            wait_EV_to_char = min(num_chargers, len(current_wait_EV)) #number of EVs which were waiting but will be charged in this timestep
            wait_EV_record.append([current_wait_EV.pop(0) for idx in range(wait_EV_to_char)]) #those EVs are no longer waiting but their wait time is recorded

            current_wait_EV = [x+1 for x in current_wait_EV] #add one hour wait to all remaining waiting EVs
            remain_chargers = num_chargers - wait_EV_to_char #chargers remaining for arriving EVs after waiting EVs have been charged
            arrive_EV_to_char = min(remain_chargers, arriving_EVs) #number of EVs which just arrived that will be charged
            arrive_EV_to_wait = arriving_EVs - arrive_EV_to_char
            total_char = wait_EV_to_char + arrive_EV_to_char
            daily_char.append(total_char)

            for n in range (arrive_EV_to_wait):
                current_wait_EV.append(1) #add the new waiting EVs with a wait time of 1 hour
        wait_EV_record.append(current_wait_EV)
        total_prev_wait_EV.append(wait_EV_record)
        char_profile.append(daily_char)
    # if (len(current_wait_EV) > 0 ):
    #     print("never charged ev wait times: " +  str(current_wait_EV))
    
    total_prev_wait_EV[1].append(current_wait_EV)
    return char_profile, total_prev_wait_EV

def optimise_chargers (yearly_arrival_times, init_chargers, allow_max_wait_time, allow_max_daily_wait_EV):
    '''
    allow_max_wait_time = maxmimum allowable length of time for any given EV to wait in hours
    allow_max_daily_wait_EV = maximum allowable number of EVs which have to wait over any given day
    '''
    num_chargers = init_chargers
    while True:
        wait_EV = char_profile(yearly_arrival_times,num_chargers)[1]
        flat_wait_EV = [item for sublist in [item for sublist in wait_EV for item in sublist] for item in sublist]
        if flat_wait_EV != []:
            max_wait_time = max(flat_wait_EV)
        else:
            max_wait_time = 0

        max_daily_wait_EV = 0
        for i in range (365):
            daily_wait_EV = 0
            for j in range(24):
                daily_wait_EV = daily_wait_EV + len(wait_EV[i][j])
            max_daily_wait_EV = max(daily_wait_EV,max_daily_wait_EV)

        if (max_wait_time <= allow_max_wait_time) and (max_daily_wait_EV<=allow_max_daily_wait_EV):
            break
        num_chargers = num_chargers + 1

    return num_chargers

def save_timeseries (data, year, filename = None):
    times = [(dt.time(i).strftime('%H:%M')) for i in range(24)]
    init_date = dt.date(year,1,1)
    day = dt.timedelta(days = 1)
    dates = [((init_date + i*day).strftime('%d/%m/%Y')) for i in range(365)]

    df = pd.DataFrame(data, index = dates, columns = times)
    df.to_csv(filename + str(year))
    return df  

def load_profile (yearly_arrival_times, charge_rate, num_chargers):
    charge_profile = np.array(char_profile(yearly_arrival_times,num_chargers)[0], dtype=object)
    load_profile = charge_rate*charge_profile
    return load_profile
