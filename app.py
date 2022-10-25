from msilib.schema import Icon
import streamlit as st
import numpy as np
import json
import helper
import plotly.graph_objects as go




def main():
    ######## Page Design Setup ###########
    st.set_page_config(layout="wide", page_title="Signal Sampling Studio")
    with open("style.css") as design:
        st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)
    title = '<h1 class="h1">Signal Sampling Studio</h1>'
    # st.markdown(title,unsafe_allow_html= True)

    ######### Variable intialization ########### 
    noise_flag = False
    sampling_points = [[0], [0]]

    with st.container():
        ####### Intializing Session state variables ##########
        labels_list = [" "]
        if 'Signals' in st.session_state:
            if st.session_state.Signals == []:
                empty_signals_flag = True
            else:
                empty_signals_flag = False
                for signal in st.session_state.Signals:
                    labels_list.append(signal["Label"])
                max_frequency = max(st.session_state.Signals, key=lambda x: x['Frequency'])["Frequency"]
        else:
            st.session_state['Signals'] = [{"Label": "default_signal", "Amplitude": 1, "Frequency": 1}]
            max_frequency =1
            empty_signals_flag = True

        ############### Expander component ############
        ######### Adding new signal tab######
        upload_col,label_col, frequency_col,amplitude_col,remove_box_col,remove_btn_col  = st.columns([1.3,0.5,0.5,0.5,0.5,0.4],gap="medium")
        with st.container():
            with label_col:
                st.subheader(" ")
                label = st.text_input("Signal Label")
            with frequency_col:
                st.write("Add New Signal")
                frequency = st.number_input("Frequency", value=1)
                add_signal = st.button("Add Signal")
            with amplitude_col:
                st.subheader(" ")
                amplitude = st.number_input("Amplitude", value=1)
        with remove_box_col:
            st.subheader(" ")
            selectbox_placeholder = st.empty()
            chosen_signal_index = selectbox_placeholder.selectbox("Choose Signal to remove", range(len(labels_list)), format_func=lambda x: labels_list[x], key="Signals selectbox")
        with remove_btn_col:
            st.subheader(" ")
            st.subheader(" ")
            remove_btn_placeholder=st.empty()
            remove_signal_btn =remove_btn_placeholder.button("🚨 Remove Signal",key="remove_btn")
        if remove_signal_btn:
            st.session_state.Signals.pop(chosen_signal_index-1)
            labels_list.pop(chosen_signal_index)
            selectbox_placeholder.selectbox("Choose Signal to edit", range(len(labels_list)), format_func=lambda x: labels_list[x],index=0)

        def new_upload():
            st.session_state["uploaded_file_flag"] = True
        with upload_col:
            with st.container():
                uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type=['json'], on_change=new_upload)
                st.warning('Any New uploading file will reset your whole work!!', icon="⚠️")
                if uploaded_file is not None and st.session_state.uploaded_file_flag:
                    uploaded_file.seek(0)
                    try:
                        uploaded_signals = json.load(uploaded_file)
                        st.session_state.Signals=uploaded_signals[0]["Signals"]
                        noise_flag=uploaded_signals[0]["Noise_flag"]
                        noise_level=uploaded_signals[0]["Noise_Value"]
                        st.session_state[ "uploaded_file_flag"]= False
                    except:
                        st.error("Improper File",icon="🚨")
        ########## Add signal button actions #############
        if add_signal:
            with amplitude_col:
                if label in labels_list or label =="":
                    st.write("Duplicate Label or empty label, please change")
                elif frequency == 0 or amplitude == 0:
                    error_msg = '<p class="error_msg">Frequency or amplitude cannot be zero</p>'
                    st.markdown(error_msg,unsafe_allow_html= True)
                else:
                    st.session_state.Signals.append({"Label": label, "Amplitude": amplitude, "Frequency": frequency})
                    labels_list.append(label)
                    max_frequency = max(st.session_state.Signals, key=lambda x: x['Frequency'])["Frequency"]

    with st.container():
        data_col, graphs_col = st.columns([1, 2], gap="medium")
        with data_col:
            st.subheader("Current Signals")
            if "Signals" in st.session_state:
                st.table(st.session_state.Signals)
            else:
                st.write("No Signals to display")
            with st.container():
                noise_flag = st.checkbox("Add Noise")
                noise_level = st.slider("Noise Level(SNR)(dB)", -100, 100, step=1, value=0, disabled=not noise_flag)
            sampling_frequency = 1
            h3 = '<h3 class="h3">Sampling & Reconstruction</h3>'
            st.markdown(h3,unsafe_allow_html= True) 
            ####### sample rate scale select box handelling##########
            frequency_mode = st.selectbox(
                "Sample Rate(HZ)", ("Normalized Frequency","Fmax"))
            if frequency_mode == "Normalized Frequency":
                start = 1.0
                end = 5.0*max_frequency
            elif frequency_mode == "Fmax":
                start = 1.0
                end = 5.0
            sampling_frequency = st.slider(" ", label_visibility="hidden",min_value=start, max_value=end, step=0.1,value=2.0,disabled=empty_signals_flag)
            if frequency_mode=="Fmax":
                sampling_frequency = sampling_frequency * max_frequency
            time = st.slider("Time displayed (s)", 0.1, 5.0, step=0.1,value=1.0)

    ############### Graphs column compenets ##########
        with graphs_col:
            main_signal = np.zeros(500)
            time_axis = np.linspace(0, time, 500)
            if 'Signals' in st.session_state:
                for signal in st.session_state.Signals:
                    main_signal += signal["Amplitude"] * \
                        np.sin(2 * np.pi * signal["Frequency"] * time_axis)
                if noise_flag:
                    main_signal += helper.add_noise(noise_level)
                sampling_points = helper.sampling_func(
                    sampling_frequency, time_axis, main_signal, time)
            main_signal_trace = go.Scatter(
                x=time_axis,
                y=main_signal,
                name='Signal'
            )
            sampling_point_trace = go.Scatter(
                x=sampling_points[0],
                y=sampling_points[1],
                mode='markers',
                name='Sample Points',
                marker = {'color' : 'red',"size":10}
            )
            reconstruct_signal = go.Scatter(
                    x=time_axis,
                    y=helper.reconstruction(time_axis, sampling_points[0], sampling_points[1]),
                    name="Reconstructed Signal",
                    marker = {'color' : 'orange'}
                )
            data = [main_signal_trace,reconstruct_signal,sampling_point_trace]
            layout = go.Layout(title=" ", xaxis={'title': 'Time(Sec)',"fixedrange": True}, yaxis={'title': 'Amplitude',"fixedrange": True})
            fig = go.Figure(data=data, layout=layout)
            fig.update_layout(width=500,height=600,legend=dict(orientation= "h",yanchor="bottom",y=1.02,xanchor="right",x=1 ))
            fig.update_xaxes(zerolinecolor="black")
            fig.update_yaxes(zerolinecolor="black")
            st.plotly_chart(fig, use_container_width=True)
            saved_data_structure = [
                    {"Noise_flag": noise_flag, "Noise_Value": noise_level, "Signals": st.session_state.Signals}]
            data_json_string = json.dumps(saved_data_structure)
        col1,col2 =st.columns([10,2])
        with col2:
            save_signals_btn = st.download_button(
                        label="Download",
                        file_name="data.json",
                        mime="application/json",
                        data=data_json_string,
                    )

if __name__ == "__main__":
    main()
