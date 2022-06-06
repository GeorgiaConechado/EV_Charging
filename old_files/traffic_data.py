import numpy as np
import pandas as pd
from EV_Charging import *


def traffic_data(year, season = 'Peak Day') :
    filename = 'traffic_data\\SA_Traffic_Model_Far_North_'+str(year)+'.csv'
    df = pd.read_csv(filename)
    print(df[season])


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

# traffic_mu_list = np.arange(0,100,2)

# num_chargers_list = []

# for i in range(len(traffic_mu_list)):
#     traffic_mu = traffic_mu_list[i]
#     traffic_sigma = traffic_mu*sigma/mu

#     yearly_arrival_times = arrival_times(traffic_mu, traffic_sigma, hourly_weightings, 0.5)
#     filename = 'arrival_times\\trend\\'+str(i)+'_'
#     save_timeseries(yearly_arrival_times,2025,filename)
#     num_chargers = optimise_chargers(yearly_arrival_times,1,1,100)
#     num_chargers_list.append(num_chargers)

# import matplotlib.pyplot as plt

# plt.plot(traffic_mu_list,num_chargers_list)
# #plt.ylabel('some numbers')
# plt.show()
# plt.savefig('graphs\\num_chargers')

# # load = load_profile(yearly_arrival_times, 100, num_chargers)
# # save_timeseries(load,2025,'load_profile\\')
