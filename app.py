import streamlit as st
import numpy as np
import helper
import plotly.graph_objects as go
import pandas  as pd
def main():
                            #___________________________Page Setup design _________________________________________#
    st.set_page_config(layout="wide", page_title="Signal Sampling Studio")
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    with open("style.css") as design:
        st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)

                            #___________________________intializing basic variables _________________________________________#
    noise_flag = False
    sampling_points = [[0], [0]]
    uploaded= False
    with st.container():
        labels_list = [" "]
        if 'Signals' in st.session_state:
            if st.session_state.Signals == []:
                empty_signals_flag = True
            else:
                empty_signals_flag = False
                for signal in st.session_state.Signals:
                    labels_list.append(signal["Label"])
                try:
                    st.session_state['max_frequency'] = max(st.session_state.Signals, key=lambda x: x['Frequency'])["Frequency"]
                except:
                    st.session_state['max_frequency']=1
                    empty_signals_flag=True
        else:
            st.session_state['Signals'] = [{"Label": "default_signal", "Amplitude": 1, "Frequency": 1}]
            labels_list.append("default_signal")
            st.session_state['max_frequency'] =1
            empty_signals_flag = False
                            #_______________________________upload /add / remove signals compenets and logic _____________________________________#
        upload_col,label_col, frequency_col,amplitude_col,remove_box_col= st.columns([1.2,0.6,0.6,0.6,0.6],gap="medium")


                            #__________________________Uploading/ delete uplaodied Functionality _________________________________________#
        with upload_col:
            with st.container():
                uploaded_file = st.file_uploader("Upload Signal", accept_multiple_files=False, type=['csv']) 
                if uploaded_file is not None :
                    ## check file is proper to deal with
                    try:
                        df = pd.read_csv(uploaded_file)
                        st.session_state['uploaded_x']=df["X"].to_numpy()
                        st.session_state['uploaded_y']=df["Y"].to_numpy()
                        st.session_state['max_frequency']=max(df["fmax"][1],st.session_state['max_frequency'])
                        empty_signals_flag = False
                        uploaded=True
                    except:
                        st.error("Improper File",icon="🚨")
                ## if file is removed from uploading box
                else:
                    st.session_state['uploaded_x']=np.linspace(0, 1, 500)
                    st.session_state['uploaded_y']=np.zeros(500)
                    uploaded=False

                            #__________________________Adding New signal Functionality _________________________________________#
        with st.container():
                            ### Add new Signal Compenets ###
            with label_col:
                label = st.text_input("Signal Label",value=("Signal_"+str(len(st.session_state.Signals))))
            with frequency_col:
                frequency = st.number_input("Frequency(HZ)", value=1, min_value=0,max_value=500)
                add_signal = st.button("Add Signal")
            with amplitude_col:
                amplitude = st.number_input("Amplitude(mV)", value=1, min_value=0,max_value=500)

                            ### Add new Signal Logic and validation check ###
        if add_signal:
            with amplitude_col:
                if label =="":
                    st.write("Label Cannot be empty")
                elif frequency == 0 or amplitude == 0:
                    error_msg = '<p class="error_msg">Frequency or amplitude cannot be zero</p>'
                    st.markdown(error_msg,unsafe_allow_html= True)
                else:
                    if label in labels_list:
                        label = label +"(1)"
                    st.session_state.Signals.append({"Label": label, "Amplitude": amplitude, "Frequency": frequency})
                    labels_list.append(label)
                    st.session_state['max_frequency'] = max(st.session_state.Signals, key=lambda x: x['Frequency'])["Frequency"]
                            #__________________________Remove signal Functionality _________________________________________#
        with remove_box_col:
                            ### remove  Signal Compenets ###
            chosen_signal_index = st.selectbox("Choose Signal to remove", range(len(labels_list)), format_func=lambda x: labels_list[x], key="Signals selectbox")
            remove_signal_btn_placeholder = st.empty()
            remove_signal_btn =remove_signal_btn_placeholder.button("🚨 Remove Signal",key="remove_btn", disabled=chosen_signal_index==0)

                            ### remove  Signal logic ###
        if remove_signal_btn:
            st.session_state.Signals.pop(chosen_signal_index-1)
            labels_list.pop(chosen_signal_index)
            remove_signal_btn_placeholder.button("🚨 Remove Signal", disabled=True)
            st.experimental_rerun()

                            #__________________________Graphing, Sampling,Reconstruction _________________________________________#
    with st.container():
        data_col, graphs_col, select_graph_col = st.columns([1, 2,0.3], gap="small")
                            #### Displaying cureent signals ####
        with data_col:
            h3 = '<h3 class="h3">Current Signals</h3>'
            st.markdown(h3,unsafe_allow_html= True) 
            st.table(st.session_state.Signals)
            with st.container():

                            #### Adding Noise Compenets ####
                noise_flag = st.checkbox("Add Noise")
                noise_level = st.slider("Noise Level(SNR)(dB)", 1, 50, step=1, value=50, disabled=not noise_flag)
            sampling_frequency = 1
            h3 = '<h3 class="h3">Sampling & Reconstruction</h3>'
            st.markdown(h3,unsafe_allow_html= True) 

                            #### Sampling Modes Handelling ####
            frequency_mode = st.selectbox(
                "Sample Rate(HZ)", ("Normalized Frequency",f"Fmax ={st.session_state['max_frequency']} Hz"))
            if frequency_mode == "Normalized Frequency":
                start = 1.0
                end = 5.0*st.session_state['max_frequency']
                format ="%f Hz"
            elif frequency_mode == f"Fmax ={st.session_state['max_frequency']} Hz":
                start = 1.0
                end = 5.0
                format ="%f Fmax"
            sampling_frequency = st.slider(" ", label_visibility="hidden",min_value=start, max_value=end, step=0.1,value=2.1,disabled=empty_signals_flag,format=format)
            if frequency_mode==f"Fmax ={st.session_state['max_frequency']} Hz":
                sampling_frequency = sampling_frequency * st.session_state['max_frequency']

                            #### displayed time Compenet ####
            # time = st.slider("Time displayed (seconds)", 0.1, 5.0, step=0.1,value=1.0,disabled=uploaded)
            time= 1
                        #__________________________Graphing _________________________________________#

        with select_graph_col:
            ##_____Check selected signals to show______________##
            st.title(" ")
            show_main_signal=st.checkbox("Main Signal",value=True)
            show_samples=st.checkbox("Sample Points",value=True)
            show_reconstructed=st.checkbox("Recnstructed",value=True)
        
        with graphs_col:
            ##_____Check if any uploaded signal to add_______________##
            if "uploaded_x" in st.session_state and st.session_state['uploaded_y'].sum() !=0:
                    time_axis=st.session_state['uploaded_x']
                    main_signal=st.session_state['uploaded_y']
            else:
                time_axis = np.linspace(0, time, int(1500*time))
                main_signal = np.zeros(int(1500*time))
            ##_____iterate over signals generated by signal generator to add_______________##
            if 'Signals' in st.session_state:
                for signal in st.session_state.Signals:
                    main_signal += signal["Amplitude"] * \
                        np.sin(2 * np.pi * signal["Frequency"] * time_axis)
                if noise_flag: # check noise to add
                    main_signal += helper.add_noise(main_signal,noise_level)
                sampling_points = helper.sampling_func(sampling_frequency, time_axis, main_signal, time)
            ###___________ Identifying different traces on graph_____######
            main_signal_trace = go.Scatter(
                x=time_axis,
                y=main_signal,
                name='Signal',
                marker = {'color' : '#5885AF'},
                visible=show_main_signal
            )
            sampling_point_trace = go.Scatter(
                x=sampling_points[0],
                y=sampling_points[1],
                mode='markers',
                name='Sample Points',
                marker = {'color' : 'red',"size":10},
                visible=show_samples
            )
            reconstruct_signal = go.Scatter(
                    x=time_axis,
                    y=helper.reconstruction(time_axis, sampling_points[0], sampling_points[1]),
                    name="Reconstructed Signal",
                    marker = {'color' : 'orange'},
                    visible=show_reconstructed
                )
            ###______________Graph Displaying _________________________###
            data = [main_signal_trace,reconstruct_signal,sampling_point_trace]
            layout = go.Layout( margin=go.layout.Margin(l=0,r=0, b=0, t=70,),xaxis={'title': 'Time(Sec)',"fixedrange": True}, yaxis={'title': 'Amplitude(mV)',"fixedrange": True})
            fig = go.Figure(data=data, layout=layout)
            fig.update_layout(width=500,height=650,legend=dict(orientation= "h",yanchor="bottom",y=1.02,xanchor="right",x=1 ))
            fig.update_xaxes(zerolinecolor="black")
            fig.update_yaxes(zerolinecolor="black")
            st.plotly_chart(fig, use_container_width=True)
        
            ###_____________________Reconstructed signal download logic _________________________###

        reconstructed_signal={
            "X": time_axis,
            "Y": helper.reconstruction(time_axis, sampling_points[0], sampling_points[1]),
            "fmax": sampling_frequency/2 if sampling_frequency/2<=st.session_state['max_frequency'] else st.session_state['max_frequency']
        }
        signal_dataframe=pd.DataFrame(reconstructed_signal)
        with data_col:
            save_signals_btn = st.download_button(
                        label="Download",
                        file_name="signal.csv",
                        mime='text/csv',
                        data=signal_dataframe.to_csv(),
                    )

if __name__ == "__main__":
    main()
