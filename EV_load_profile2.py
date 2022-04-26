import datetime as dt
from doctest import Example
from turtle import shape
import numpy as np
import pandas as pd

hourly_weight = [2,2,1,1,1,1,3,7,14,20,23,27,26,25,23,17,13,8,5,3,3,2,2,2] #example taken from stuart highway evernergi report

def arrival_times(traffic_mu, traffic_sigma, hourly_weight, stop_prob = 1):
    yearly_arrival_times = []    
    for i in range (365):
        daily = []
        traffic = np.round(np.random.normal(loc= traffic_mu, scale = traffic_sigma))
        arrival_times = np.random.choice(24,size=int(traffic*stop_prob),p=probability(hourly_weight))
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
        prev_wait_EV = []
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
        total_prev_wait_EV.append(prev_wait_EV)
        char_profile.append(daily_char)
    #print(len(total_prev_wait_EV[0]))
    return char_profile, total_prev_wait_EV

#char_profile(arrival_times(30,5,hourly_weight),3)

def optimise_chargers (yearly_arrival_times, init_chargers, allow_max_wait_time, allow_max_daily_wait_EV):
    '''
    allow_max_wait_time = maxmimum allowable length of time for any given EV to wait in hours
    allow_max_daily_wait_EV = maximum allowable number of EVs which have to wait over any given day
    '''
    num_chargers = init_chargers
    wait_EV = char_profile(yearly_arrival_times,num_chargers)[1]
    print(wait_EV)[0]
    #max_wait_time = np.max(np.max(np.max(wait_EV)))
    # print(max_wait_time)
    flat_wait_EV = [item for sublist in [item for sublist in wait_EV for item in sublist] for item in sublist]
    if flat_wait_EV != []:
        max_wait_time = max(flat_wait_EV)
    else:
        max_wait_time = 0
    # print(max_wait_time)

    max_daily_wait_EV = 0
    for i in range (365):
        #print(wait_EV[i])
        daily_wait_EV = 0
        for j in range(24):
            daily_wait_EV = daily_wait_EV + len(wait_EV[i][j])
        max_daily_wait_EV = max(daily_wait_EV,max_daily_wait_EV)
    #print(max_daily_wait_EV)
    
    #while 

    return num_chargers

yearly_arrival_times = arrival_times(30,5,hourly_weight)
#print(yearly_arrival_times)
optimise_chargers(yearly_arrival_times,4,1,5)

#need to fix issue if waitEV list is empty