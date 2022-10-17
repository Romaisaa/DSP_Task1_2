
import streamlit as st 
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
import wave
from helper import sampling_func
from helper import plotting_style


def main():
    st.set_page_config(page_title="Signal Sampling Studio")

                            ############ Signal generator Compenets ###########################
    st.title("Signal Generator")
    frequency = st.slider("Signal Frequency(Hz)", 0, 100)
    amplitude= st.slider("Signal Amplitude",0,200)
    time= st.slider("Time dispalyed (s)", 0.0, 5.0)
    sampling_frequency=1
    

                            ################### Sampling Compenents #############################
    st.title("Sampling  Functionality")
    c1,c2= st.columns([20,40])
    with st.container():
        with c1:
            frequency_mode = st.selectbox("Sample Rate(HZ)",("Normailzed Frequency","Fmax")) 
            
        with c2:
            if frequency_mode=="Normailzed Frequency":
                start=1
                end=100
                sampling_frequency= st.slider(" ",label_visibility="hidden" ,min_value=start, max_value=end)
            elif frequency_mode=="Fmax":
                start=1.0
                end = 5.0
                s_value= st.slider(" ",label_visibility="hidden" ,min_value=start, max_value=end)
                sampling_frequency=s_value * frequency
            sampling_points=sampling_func(frequency,sampling_frequency, time, amplitude)



                            ######################  Signal Generator & Graphing ######################33   
        f1 = lambda x: amplitude*np.sin(frequency*2*np.pi*x)
        x = np.linspace(0,time,500)
        sampled_f1 = [f1(i) for i in x]
        fig = plotting_style(x,sampled_f1, "scatter",sampling_points[0],sampling_points[1])
        st.pyplot(fig)



                            #################  Uploading Audio with graphing   ###################### 
    st.title("Open External Signal")
    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)

    if uploaded_file is not None: 
        obj = wave.open(uploaded_file.name,"rb")
        sample_freq= obj.getframerate()
        n_samples = obj.getnframes()
        single_wave=obj.readframes(-1)
        obj.close()

        t_audio= n_samples/sample_freq
        signal_array = np.frombuffer(single_wave, dtype=np.int16)
        times = np.linspace(0,t_audio, num=n_samples*2)
        fig = plotting_style(times,signal_array)
        st.pyplot(fig)







if __name__=="__main__":
    main()
