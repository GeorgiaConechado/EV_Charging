import datetime as dt
from doctest import Example
import numpy as np
import pandas as pd


def arrival_times(traffic_mu, traffic_sigma, hourly_weight, stop_prob = 1):
    traffic = np.round(np.random.normal(loc= traffic_mu, scale = traffic_sigma))
    arrival_times = np.random.choice(24,size=int(traffic*stop_prob),p=probability(hourly_weight))

    yearly_arrival_times = []    
    for i in range (365):
        daily = []
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
    char = []
    current_wait_EV = []
    prev_wait_EV = []

    for i in range(len(yearly_arrival_times)):
        daily_char = []
        daily_times = yearly_arrival_times[i]
        for j in range(len(daily_times)):
            #print(j)
            arriving_EVs = daily_times[j]
            #print("arriving EVs:", arriving_EVs)
            wait_EV_to_char = min(num_chargers, len(current_wait_EV)) #number of EVs which were waiting but will be charged in this timestep
            #print('wait EV to char:', wait_EV_to_char)

            prev_wait_EV.append([current_wait_EV.pop(0) for idx in range(wait_EV_to_char)]) #those EVs are no longer waiting but their wait time is recorded

            current_wait_EV = [x+1 for x in current_wait_EV] #add one hour wait to all remaining waiting EVs
            #print('current wait EV:', current_wait_EV)
            remain_chargers = num_chargers - wait_EV_to_char #chargers remaining for arriving EVs after waiting EVs have been charged
            arrive_EV_to_char = min(remain_chargers, arriving_EVs) #number of EVs which just arrived that will be charged
            #print('arriving EVs to be charged:',arrive_EV_to_char)
            arrive_EV_to_wait = arriving_EVs - arrive_EV_to_char
            #print('arriving EVs to wait', arrive_EV_to_wait)
            total_char = wait_EV_to_char + arrive_EV_to_char
            daily_char.append(total_char)

            for n in range (arrive_EV_to_wait):
                current_wait_EV.append(1) #add the new waiting EVs with a wait time of 1 hour
            #print('final current waiting EV', current_wait_EV)

        char.append(daily_char)
    print(prev_wait_EV)
    return char, prev_wait_EV

#char_profile(arrival_times(30,5,[2,2,1,1,1,1,3,7,14,20,23,27,26,25,23,17,13,8,5,3,3,2,2,2]),3)

# def optimise_chargers (yearly_arrival_times, init_chargers, acceptable_wait):
    
#     return num_chargers