from EV_load_profile2 import *
import pandas as pd

year = 2025

filename = 'traffic_data\\SA_Traffic_Model_Far_North_'+str(year)+'.csv'
df = pd.read_csv(filename)
df['yearly mean'] = df.iloc[:, 1:9].mean(axis=1)
hourly_weightings = df['yearly mean'].to_list()

traffic_mu = 51
traffic_sigma = 19.78

yearly_arrival_times = arrival_times(traffic_mu, traffic_sigma, hourly_weightings, 0.5)
save_timeseries(yearly_arrival_times,2025,'arrival_times\\')

num_chargers = optimise_chargers(yearly_arrival_times,4,1,20)
print(num_chargers)