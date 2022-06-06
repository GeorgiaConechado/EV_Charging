from EV_Charging import *
import pandas as pd

year = 2025

filename = 'traffic_data\\SA_Traffic_Model_Far_North_'+str(year)+'.csv'
df = pd.read_csv(filename)
df['yearly mean'] = df.iloc[:, 1:9].mean(axis=1)
hourly_weightings = df['yearly mean'].to_list()

mu = 51
sigma = 19.78

traffic_mu = 1
traffic_sigma = traffic_mu*sigma/mu

yearly_arrival_times = arrival_times(traffic_mu, traffic_sigma, hourly_weightings, 0.5)
save_timeseries(yearly_arrival_times,2025,'arrival_times\\')

#print(yearly_arrival_times)

num_chargers = optimise_chargers(yearly_arrival_times,1,1,100)
print(num_chargers)

load = load_profile(yearly_arrival_times, 100, num_chargers)
save_timeseries(load,2020,'load_profile\\')

traffic_mu_list = np.arange(0,100,2)

num_chargers_list = []

for i in range(len(traffic_mu_list)):
    traffic_mu = traffic_mu_list[i]
    traffic_sigma = traffic_mu*sigma/mu

    yearly_arrival_times = arrival_times(traffic_mu, traffic_sigma, hourly_weightings, 0.5)
    filename = 'arrival_times\\trend\\'+str(i)+'_'
    save_timeseries(yearly_arrival_times,2025,filename)
    num_chargers = optimise_chargers(yearly_arrival_times,1,1,100)
    num_chargers_list.append(num_chargers)

import matplotlib.pyplot as plt

plt.plot(traffic_mu_list,num_chargers_list)
#plt.ylabel('some numbers')
plt.show()
plt.savefig('graphs\\num_chargers')

# load = load_profile(yearly_arrival_times, 100, num_chargers)
# save_timeseries(load,2025,'load_profile\\')
