import numpy as np
import random
def sampling_func(Sampling_Freq, time_points, signals_points,time):
    total_second_points=len(time_points)/time
    sample_step_size=total_second_points/Sampling_Freq
    sampled_time=time_points[::int(sample_step_size)]
    sampled_signal=signals_points[::int(sample_step_size)]

    return sampled_time, sampled_signal



def add_noise(SNR):
    noise_amp = 0
    if SNR >= 0:
        noise_amp = 0.00008/(SNR+1)
    else:
        noise_amp = -1 * SNR * 0.0017

    noise = noise_amp * np.asarray(random.sample(range(0, 500), 500))

    return noise

def reconstruction(t, frquency_rate, sample_points, y_sampled):
    reconstructed_func = 0
    for i in range(0, sample_points, 1):
        reconstructed_func += y_sampled[i] * np.sinc(t*frquency_rate-i)
    return reconstructed_func
