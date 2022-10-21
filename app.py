from symbol import parameters
import streamlit as st
import numpy as np 
import pandas as pd
import json

def main():
    st.set_page_config(layout="wide",page_title="Signal Sampling Studio")
    with open("style.css") as design:
        st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)
    st.title("Signal Sampling Studio")
    noise_flag=False
    with st.container():
        labels_list=[" "]
        if 'Signals' in st.session_state:
            for signal in st.session_state.Signals:
                labels_list.append(signal["Label"]) 
        with st.expander("Signal Composer"):
            upload_signal,add_new_signal, edit_signal, noise_addition = st.tabs(["Upload new Signal","Add new Siganl", "Edit Signal", "Nosie Level"])
            with edit_signal:
                if st.session_state.Signals!=[" "]:
                    selectbox_placeholder=st.empty()
                    chosen_signal_index= selectbox_placeholder.selectbox("Choose Signal to edit", range(len(labels_list)), format_func=lambda x: labels_list[x], key="Signals selectbox")
                    if chosen_signal_index != 0 and st.session_state.Signals!=[" "] :
                        frequency_value= st.session_state.Signals[chosen_signal_index-1]["Frequency"]
                        amplitude_value=st.session_state.Signals[chosen_signal_index-1]["Amplitude"]
                        edit_col1,edit_col2=st.columns([1,1])
                        with edit_col1:
                            new_frequency=st.number_input("New Frequency",value=frequency_value, step=1)
                            remove_signal_btn=st.button("Remove Signal")
                        with edit_col2:
                            new_amplitude=st.number_input("New Amplitude",value=amplitude_value,step=1)
                            edit_signal_btn=st.button("Update Signal")
                        if edit_signal_btn:
                            st.session_state.Signals[chosen_signal_index-1]["Frequency"]=new_frequency
                            st.session_state.Signals[chosen_signal_index-1]["Amplitude"]=new_amplitude
                        if remove_signal_btn:
                            st.session_state.Signals.pop(chosen_signal_index-1)
                            chosen_signal_index=selectbox_placeholder.selectbox("Choose Signal to edit", range(len(labels_list)), format_func=lambda x: labels_list[x], index=0)
                else:
                    st.write("No signals are added ")
            with add_new_signal:
                parameters_col,range_col=st.columns([2,1])
                with range_col:
                    st.write(" ")
                    st.write(" ")
                    st.write(" ")
                    st.write(" ")
                    st.write(" ")
                    st.write(" ")
                    frequency_range= st.number_input("Frequency Range",value=100)
                    amplitude_range= st.number_input("Amplitude Range",value=500)
                    add_signal =st.button("Add Signal")        
                with parameters_col:
                    label= st.text_input("Signal Label")
                    frequency_placeholder = st.empty()
                    frequency = frequency_placeholder.slider("Signal Frequency(Hz)", 0, frequency_range, key="frequency_slider",value=0)
                    amplitude_placeholder = st.empty()
                    amplitude= amplitude_placeholder.slider("Signal Amplitude",0,amplitude_range, key="amplitude_slider",value=0)
                if add_signal:
                    empty_col,warning_col=st.columns([3,1])
                    with warning_col:
                        if label in labels_list:
                            st.write("Duplicate Label or empty label, please change")
                        elif frequency==0 or amplitude==0:
                            st.write("Frequency or amplitude cannot be zero")
                        else:
                            if 'Signals' not in st.session_state:
                                st.session_state['Signals'] = [{ "Label":label,"Amplitude":amplitude, "Frequency":frequency}]
                            else:
                                st.session_state.Signals.append({ "Label":label,"Amplitude":amplitude, "Frequency":frequency})
                            frequency=frequency_placeholder.slider("Signal Frequency(Hz)",0,amplitude_range,value=0)
                            amplitude= amplitude_placeholder.slider("Signal Amplitude",0,amplitude_range, value=0)          
            with noise_addition:
                noise_flag= st.checkbox("Add Noise to current Signal")
                noise_range=1
                noise_slider_col,noise_range_col=st.columns([2,1])
                with noise_slider_col:
                    noise_level=st.slider("Noise Level(SNR)", 0,100, step=1, value=noise_range, disabled=not noise_flag)
                with noise_range_col:
                    noise_range=st.number_input("Noise Range", value=100, disabled=not noise_flag)
            with upload_signal:
                uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)


    with st.container():
        data_col, graphs_col = st.columns([1,2],gap="medium")
        with data_col:
            st.header("Current Signals")
            if "Signals" in st.session_state:
                st.table(st.session_state.Signals)
                data_json_string = json.dumps(st.session_state.Signals)
                save_signals_btn=st.download_button(
                    label="Download Current Signals",
                    file_name="data.json",
                    mime="application/json",
                    data=data_json_string,
                )
            else:
                st.write("No Signals to display")
                
            st.header("Sampling & Reconstruction")
            frequency_mode = st.selectbox("Sample Rate(HZ)",("Normailzed Frequency","Fmax")) 
            if frequency_mode=="Normailzed Frequency":
                start=1
                end=100
                sampling_frequency= st.slider(" ",label_visibility="hidden" ,min_value=start, max_value=end)
            elif frequency_mode=="Fmax":
                start=1.0
                end = 5.0
                s_value= st.slider(" ",label_visibility="hidden" ,min_value=start, max_value=end)
            time= st.slider("Time dispalyed (s)", 0.0, 5.0, value=1.0)
            reconstruct_btn=st.button("Reconstruct")
        with graphs_col:
            st.title(" ")
            chart_data = pd.DataFrame(
            np.random.randn(50, 3),
            columns=["a", "b", "c"])
            st.bar_chart(chart_data)
            chart_data = pd.DataFrame(
            np.random.randn(50, 3),
            columns=["a", "b", "c"])
            st.bar_chart(chart_data)

if __name__=="__main__":
    main()