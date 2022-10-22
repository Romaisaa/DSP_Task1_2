import numpy as np
import random


def sampling_func(Sampling_Freq, time, signals):
    sampled_func = 0
    n = np.linspace(0, time, int(time*Sampling_Freq))
    for signal in signals:
        sampled_func += signal["Amplitude"] * \
            np.sin(2 * np.pi * signal["Frequency"] * n)
    return n, sampled_func


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
