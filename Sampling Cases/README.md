# Nyquist theorem

## Table of contents

- [Overview](#overview)
- [Examples](#examples)
- [concolusion](#concolusion)

## Overview

The Nyquist theorem specifies that a sinuisoidal function in time or distance can be regenerated with no loss of information as long as it is sampled at a frequency greater than or equal to twice per cycle.
<br>
which means that if fs more than or equal the max frequency in the signal, the signal can be reconstructed with no loss of main signal
<br>
<br>

## Examples

- Applying different sampling frequency on signal with 2 added signals(2Hz & 6Hz)
<p align="center">
 <img src="main_signal.png"/>
</p>
1- Sampling at nyquist frequency (Fs = 12 Hz)<br>
<p align="center">
 <img src="sampling_12Hz.png"/>
</p>
2- Undersampling at (Fs = 4 Hz) 
&emsp; 
<p align="center">
 <img src="sampling_4Hz.png"/>
</p>
3- Oversampling with pure signal (No noise)at (Fs = 30 Hz) 
<p align="center">
 <img src="sampling_30Hz_without_noise.png"/>
</p>

4- Oversampling with noised signal at (Fs = 30 Hz)

<p align="center">
 <img src="sampling_30Hz_with_noise_2.png"/>
<img src="sampling_30Hz_with_noise.png"/>
</p>
  <br>
  <br>

## Concolusion

Sampling at exact nyquist rate or higher with a pure signal(no noise) can effectively expresss the whole main signal, while undersampling narrow the vision of signal to fs/2 frequency only (frequencies higher than fs/2 can not be noticed).
<br>
Oversamplig appears to be perfect, but we cannot have a pure noise whole the time. Oversampling with a noised signal will lead to high effects on reconstruted signal.
