import matplotlib
import numpy as np
import wave
import math
from matplotlib import pyplot as plt
import random
import plotly
def sampling_func(Sampling_Freq, time, signals):
    x2 = 0
    T = 1 / Sampling_Freq
    n = np.arange(0, time / T)
    nT = n * T
    for signal in signals:
        x2+=signal["Amplitude"]*np.sin(2 * np.pi * signal["Frequency"] * nT)
    return nT, x2


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



