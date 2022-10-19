
import streamlit as st 
import numpy as np
import wave
from helper import sampling_func
from helper import plotting_style


def main():
    st.set_page_config(page_title="Signal Sampling Studio")  
        ############ Signal generator ###########################
    st.title("Signal Generator")
    # frequency_placeholder = st.empty()
    # amplitude_placeholder = st.empty()

    with st.container():
        frequency = st.slider("Signal Frequency(Hz)", 0, 100, key="frequency_slider",value=0)
        amplitude= st.slider("Signal Amplitude",0,200, key="amplitude_slider",value=0)
        col,check_btn_col =  st.columns([100,18])
        with check_btn_col:
            add_signal =st.button("Add Signal")
        if add_signal:
            # frequency_placeholder.slider("Signal Frequency(Hz)",value=0)
            # amplitude_placeholder.slider("Signal Amplitude",0,200, value=0)

            if 'Signals' not in st.session_state:
                st.session_state['Signals'] = [{"Amplitude":amplitude, "Frequency":frequency}]
            else:
                st.session_state.Signals.append({"Amplitude":amplitude, "Frequency":frequency})    
                    
                    
    st.title("Sampling  Functionality")
    time= st.slider("Time dispalyed (s)", 0.0, 5.0, value=1.0)
    sampling_frequency=1
    max_frequency=1
    

                            ################### Sampling Compenents #############################
    
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
                max_frequency =max(st.session_state.Signals, key=lambda x:x['Frequency'])["Frequency"]
                sampling_frequency=s_value * max_frequency
            if 'Signals'  in st.session_state:
                sampling_points=sampling_func(max_frequency,sampling_frequency, time, st.session_state.Signals)
            else:
                sampling_points=[0,0]




                            ######################  Signal Generator & Graphing ######################
        sinewave=0
        time_axis = np.linspace(0,time,500)        
        f1 = lambda time_point: amplitude*np.sin(frequency*2*np.pi*time_point)
        sampled_f1 = [f1(i) for i in time_axis]
        # sampled_f1+=sinewave
        if 'Signals'  in st.session_state:
            for signal in st.session_state.Signals:
                sinewave += signal["Amplitude"] * np.sin(2 * np.pi * signal["Frequency"] * time_axis )
            sampled_f1+=sinewave
        fig = plotting_style(time_axis,sampled_f1, "scatter",sampling_points[0],sampling_points[1])
        st.pyplot(fig)

if __name__=="__main__":
    main()
