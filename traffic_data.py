import numpy as np
import pandas as pd
from EV_load_profile2 import *


def traffic_data(year, season = 'Peak Day') :
    filename = 'traffic_data\\SA_Traffic_Model_Far_North_'+str(year)+'.csv'
    df = pd.read_csv(filename)
    print(df[season])
    # mu = 
    # sigma = 
    # weightings = df[season].tolist()
    # return {"mu":mu, "sigma":sigma, "weightings": weightings}

#traffic_data(2030)

year = 2025
season = 'Peak Day'

filename = 'traffic_data\\SA_Traffic_Model_Far_North_'+str(year)+'.csv'
df = pd.read_csv(filename)
df['yearly mean'] = df.iloc[:, 1:9].mean(axis=1)
hourly_weightings = df['yearly mean'].to_list()
# print(hourly_weightings)

if year == 2025:
    traffic_mu = 37 # between Coober Pedy and NT border
elif year == 2030:
    traffic_mu = 122 


# while True:
#     traffic_sigma = 

yearly_arrival_times = arrival_times(traffic_mu, 30, hourly_weightings)


max_traffic = 0
for i in range (365):
    max_traffic = max(sum(yearly_arrival_times[i]), max_traffic)

print(max_traffic)
print(df['Peak Day'].sum())
