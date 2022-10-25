import numpy as np
import random


########### Sampling_Func#####
# Function used to sample function points depending on sample frequencty 
# retuen: List composed of 2 lists include sampling points as list of x_values and list of y_values
# parameters:- 
# Sampling_freq-> rate of sampling
# time_points-> values of time 
# signals_points-> values of signal at each tim coressponding to time poits
# time-> time needed to be displayed for user(Graphing Time)       
def sampling_func(Sampling_Freq, time_points, signals_points,time):
    total_second_points=len(time_points)/time
    sample_step_size=total_second_points/Sampling_Freq
    sampled_time=time_points[::int(sample_step_size)]
    sampled_signal=signals_points[::int(sample_step_size)]
    return sampled_time, sampled_signal



def add_noise(SNR):
    if SNR == 0:
        noise_amp = 1
    else:
        noise_amp = 0.001/SNR
    noise = noise_amp * np.asarray(random.sample(range(0, 500), 500))
    return noise

def reconstruction(time_axis, x_sampled, sample_rate):
    if (len(x_sampled)<2):
        return [0]
    scalar = np.isscalar(time_axis)
    if scalar:
        time_axis = np.array(time_axis)
        time_axis.resize(1)
    u = np.resize(time_axis, (len(x_sampled), len(time_axis)))
    v = (x_sampled - u.T) / (x_sampled[1] - x_sampled[0])
    m = sample_rate * np.sinc(v)
    sample_rate_at_x = np.sum(m, axis=1)
    if scalar:
        return float(sample_rate_at_x)
    return sample_rate_at_x