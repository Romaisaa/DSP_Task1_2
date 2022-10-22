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
        noise_amp = 0.0008/(SNR+0.01)
    else:
        noise_amp = -1 * SNR * 0.0017
    noise = noise_amp * np.asarray(random.sample(range(0, 1000), 500))
    return noise

def reconstruction(t, frquency_rate, sample_points, y_sampled):
    time_rate = 1/frquency_rate
    y = 0
    for i in range(0, sample_points, 1):
        y += y_sampled[i] * \
            np.sin(np.pi*frquency_rate*(t - i*time_rate)) / \
            ((np.pi*frquency_rate*(t - i*time_rate)))
    return y

