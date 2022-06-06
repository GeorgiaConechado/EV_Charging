from EV_Charging import *
import pandas as pd

##############################
# Inputs
year = 2025
traffic_mu = 51
traffic_sigma = 18.78

##############################

# mu = 51
# sigma = 19.78
# for other years:
# traffic_mu = 
# traffic_sigma = traffic_mu*sigma/mu

#import traffic data 
filename = 'traffic_data\\SA_Traffic_Model_Far_North_'+str(year)+'.csv'
df = pd.read_csv(filename)
df['yearly mean'] = df.iloc[:, 1:9].mean(axis=1)
hourly_weightings = df['yearly mean'].to_list()

#generate timeseries file with arrival times
yearly_arrival_times = arrival_times(traffic_mu, traffic_sigma, hourly_weightings, 0.5)
save_timeseries(yearly_arrival_times,2025,'arrival_times\\')
#print(yearly_arrival_times)

#determine necessary number of chargers
num_chargers = optimise_chargers(yearly_arrival_times,1,1,100)
print(num_chargers)

#generate load profile timeseries
load = load_profile(yearly_arrival_times, 100, num_chargers)
save_timeseries(load,2020,'load_profile\\')