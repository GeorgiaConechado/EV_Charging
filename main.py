from EV_Charging import *
import pandas as pd

##############################
# Inputs
year = 2025
traffic_mu = 51 #given
traffic_sigma = 19.78 #calculated from traffic data peak day 

stopping_probability = 0.5 

charge_rate = 100 #kWh
charge_time = 1 # 1 hour - this can't be changed currently

allow_max_wait_time = 1 #hours
allow_max_daily_wait_EV = 100 #number of EVs

filename = 'Test_' #for saving timeseries data - without a filename the default title is the year
##############################

# mu = 51
# sigma = 19.78
# for other years:
# traffic_mu = 
# traffic_sigma = traffic_mu*sigma/mu

#import traffic data 
input_data = 'traffic_data\\SA_Traffic_Model_Far_North_'+str(year)+'.csv'
df = pd.read_csv(input_data)
df['yearly mean'] = df.iloc[:, 1:9].mean(axis=1)
hourly_weightings = df['yearly mean'].to_list()

#generate timeseries file with arrival times
yearly_arrival_times = arrival_times(traffic_mu, traffic_sigma, hourly_weightings, stopping_probability)
save_timeseries(yearly_arrival_times,year,'arrival_times\\'+filename)
#print(yearly_arrival_times)

#determine necessary number of chargers
num_chargers = optimise_chargers(yearly_arrival_times,1,allow_max_wait_time,allow_max_daily_wait_EV)
print(num_chargers)

#generate load profile timeseries
load = load_profile(yearly_arrival_times, charge_rate, num_chargers)
save_timeseries(load,year,'load_profile\\'+filename)