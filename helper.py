
import re
import matplotlib
import numpy as np
import wave, math
from matplotlib import pyplot as plt


def sampling_func(max_freq, Sampling_Freq, time,signals):
    x2=0
    T = 1 / Sampling_Freq
    n = np.arange(0, time / T)
    nT = n * T
    for signal in signals:
        x2+=signal["Amplitude"]*np.sin(2 * np.pi * signal["Frequency"] * nT)
    return nT, x2

def plotting_style(x_points, y_points, style="",x2=0,y2=0):
    fig, ax = plt.subplots()
    plt.figure(figsize=(15,5))
    ax.plot(x_points,y_points)
    if style=="scatter":
        ax.scatter(x2,y2)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    return fig