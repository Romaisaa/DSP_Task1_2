from select import select
import streamlit as st
import numpy as np 
import json
import helper 
import plotly.graph_objects as go


def main():
    st.set_page_config(layout="wide",page_title="Signal Sampling Studio")
    with open("style.css") as design:
        st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)
    st.title("Signal Sampling Studio")
    noise_flag=False
    sampling_points=[[0],[0]]
    if "uploaded_file_flag"  not in st.session_state:
        st.session_state[ "uploaded_file_flag"]= True
    with st.container():
        labels_list=[" "]
        if 'Signals' in st.session_state:
            if st.session_state.Signals==[]:
                empty_signals_flag=True
            else:    
                empty_signals_flag=False
                for signal in st.session_state.Signals:
                    labels_list.append(signal["Label"])
                max_frequency =max(st.session_state.Signals, key=lambda x:x['Frequency'])["Frequency"]
        else:
            empty_signals_flag=True
            
        with st .expander("Signal Composer"):
            upload_signal,add_new_signal, edit_signal, noise_addition = st.tabs(["Upload new Signal","Add new Siganl", "Edit Signal", "Nosie Level"])
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
                            labels_list.append(label)
                            frequency=frequency_placeholder.slider("Signal Frequency(Hz)",0,amplitude_range,value=0, step=10)
                            amplitude= amplitude_placeholder.slider("Signal Amplitude",0,amplitude_range, value=0,step=10)        
            with edit_signal:
                if labels_list!=[" "]:
                    selectbox_placeholder=st.empty()
                    chosen_signal_index= selectbox_placeholder.selectbox("Choose Signal to edit", range(len(labels_list)), format_func=lambda x: labels_list[x], key="Signals selectbox")
                    if chosen_signal_index != 0 and st.session_state.Signals!=[" "] :
                        frequency_value= st.session_state.Signals[chosen_signal_index-1]["Frequency"]
                        amplitude_value=st.session_state.Signals[chosen_signal_index-1]["Amplitude"]
                        edit_col1,edit_col2=st.columns([1,1])
                        with edit_col1:
                            new_frequency=st.number_input("New Frequency",value=frequency_value, step=1)
                            remove_signal_btn=st.button("Remove Signal")
                            if remove_signal_btn:
                                st.session_state.Signals.pop(chosen_signal_index-1)
                                labels_list.pop(chosen_signal_index)
                                # st.experimental_rerun()
                        with edit_col2:
                            new_amplitude=st.number_input("New Amplitude",value=amplitude_value,step=1)
                            edit_signal_btn=st.button("Update Signal")
                            if edit_signal_btn:
                                st.session_state.Signals[chosen_signal_index-1]["Frequency"]=new_frequency
                                st.session_state.Signals[chosen_signal_index-1]["Amplitude"]=new_amplitude
                else:
                    st.write("No signals are added ")
            with noise_addition:
                noise_flag= st.checkbox("Add Noise to current Signal")
                noise_range=100
                noise_slider_col,noise_range_col=st.columns([2,1])
                with noise_slider_col:
                    noise_level=st.slider("Noise Level(SNR)", -noise_range,noise_range, step=1, value=0, disabled=not noise_flag)
                with noise_range_col:
                    noise_range=st.number_input("Noise Range", value=100, disabled=not noise_flag)
            with upload_signal:
                def new_upload():
                    st.session_state[ "uploaded_file_flag"]=True
                uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False,type=['json'], on_change=new_upload)
                if uploaded_file is not None and st.session_state.uploaded_file_flag:
                    uploaded_file.seek(0)
                    uploaded_signals = json.load(uploaded_file)
                    st.session_state.Signals=uploaded_signals[0]["Signals"]
                    noise_flag=uploaded_signals[0]["Noise_flag"]
                    noise_level=uploaded_signals[0]["Noise_Value"]
                    st.session_state[ "uploaded_file_flag"]= False
                    



    with st.container():
        data_col, graphs_col = st.columns([1,2],gap="medium")
        with data_col:
            st.header("Current Signals")
            if "Signals" in st.session_state:
                st.table(st.session_state.Signals)
                saved_data_structure= [{"Noise_flag":noise_flag, "Noise_Value":noise_level, "Signals":st.session_state.Signals}]
                data_json_string = json.dumps(saved_data_structure)
                save_signals_btn=st.download_button(
                    label="Download Current Signal",
                    file_name="data.json",
                    mime="application/json",
                    data=data_json_string,
                )
            else:
                st.write("No Signals to display")
            sampling_frequency=1
            st.header("Sampling & Reconstruction")
            frequency_mode = st.selectbox("Sample Rate(HZ)",("Normailzed Frequency","Fmax")) 
            if frequency_mode=="Normailzed Frequency":
                start=1
                end=100
                sampling_frequency= st.slider(" ",label_visibility="hidden" ,min_value=start, max_value=end, disabled=empty_signals_flag)
            elif frequency_mode=="Fmax":
                start=1.0
                end = 5.0
                s_value= st.slider(" ",label_visibility="hidden" ,min_value=start, max_value=end, disabled=empty_signals_flag)
                if empty_signals_flag:
                    sampling_frequency=1
                else:
                    sampling_frequency=s_value * max_frequency
            time= st.slider("Time dispalyed (s)", 0.0, 5.0, value=1.0)
            reconstruct_btn=st.button("Reconstruct")
            if 'Signals'  in st.session_state:
                sampling_points=helper.sampling_func(sampling_frequency, time, st.session_state.Signals)

        with graphs_col:
            st.title(" ")
            sinewave=np.zeros(500)
            time_axis = np.linspace(0,time,500)            
            if 'Signals'  in st.session_state:
                for signal in st.session_state.Signals:
                    sinewave += signal["Amplitude"] * np.sin(2 * np.pi * signal["Frequency"] * time_axis )
                if noise_flag:
                    sinewave+=helper.add_noise(noise_level)
                    # sampling_points=helper.sampling_func(time_axis,sine)
            trace0 = go.Scatter(
            x = time_axis,
            y = sinewave,
            name='Signal'
            )
            trace1 = go.Scatter(
            x = sampling_points[0],
            y = sampling_points[1],
            mode = 'markers',
            name = 'Sample Points'
            )
            data = [trace0, trace1]
            layout = go.Layout(title = "Signal With Sampling", xaxis = {'title':'Time'}, yaxis = {'title':'Amplitude'})
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig,use_container_width=True)
            if reconstruct_btn:
                trace2= go.Scatter(
                    x=time_axis,
                    y= helper.reconstruction(time_axis,sampling_frequency,len(sampling_points[0]),sampling_points[1]),
                    name= "Reconstructed Points"
                )
                data= [trace2]
                layout=go.Layout(title = "Reconstructed signal", xaxis = {'title':'Time'}, yaxis = {'title':'Amplitude'})
                fig = go.Figure(data = data, layout = layout)
                st.plotly_chart(fig,use_container_width=True)

if __name__=="__main__":
    main()