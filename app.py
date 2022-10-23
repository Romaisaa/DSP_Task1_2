import streamlit as st
import numpy as np
import json
import helper
import plotly.graph_objects as go




def main():
    st.set_page_config(layout="wide", page_title="Signal Sampling Studio")
    with open("style.css") as design:
        st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)
    title = '<h1 class="h1">Signal Sampling Studio</h1>'
    st.markdown(title,unsafe_allow_html= True)
    noise_flag = False
    sampling_points = [[0], [0]]
    with st.container():
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
            empty_signals_flag = True

        with st .expander("Signal Composer"):
            upload_signal, add_new_signal, edit_signal, noise_addition = st.tabs(
                ["Upload new Signal", "Add new Siganl", "Edit Signal", "Nosie Level"])
            with add_new_signal:
                label = st.text_input("Signal Label")
                parameters_col, range_col = st.columns([2, 1])
                with range_col:
                    frequency_range = st.number_input("Frequency Range", value=100)
                    amplitude_range = st.number_input("Amplitude Range", value=500)
                    add_signal = st.button("Add Signal")
                with parameters_col:
                    frequency_placeholder = st.empty()
                    frequency = frequency_placeholder.slider("Signal Frequency(Hz)", 0, frequency_range, key="frequency_slider", value=0)
                    amplitude_placeholder = st.empty()
                    amplitude = amplitude_placeholder.slider("Signal Amplitude", 0, amplitude_range, key="amplitude_slider", value=0)
                if add_signal:
                    with range_col:
                        if label in labels_list or label =="":
                            st.write("Duplicate Label or empty label, please change")
                        elif frequency == 0 or amplitude == 0:
                            error_msg = '<p class="error_msg">Frequency or amplitude cannot be zero</p>'
                            st.markdown(error_msg,unsafe_allow_html= True)
                        else:
                            if 'Signals' not in st.session_state:
                                st.session_state['Signals'] = [{"Label": label, "Amplitude": amplitude, "Frequency": frequency}]
                            else:
                                st.session_state.Signals.append(
                                    {"Label": label, "Amplitude": amplitude, "Frequency": frequency})
                            labels_list.append(label)
                            frequency = frequency_placeholder.slider("Signal Frequency(Hz)", 0, amplitude_range, value=0, step=10)
                            amplitude = amplitude_placeholder.slider("Signal Amplitude", 0, amplitude_range, value=0, step=10)
                            empty_signals_flag=False
            with edit_signal:
                if labels_list != [" "]:
                    selectbox_placeholder = st.empty()
                    chosen_signal_index = selectbox_placeholder.selectbox("Choose Signal to edit", range(
                        len(labels_list)), format_func=lambda x: labels_list[x], key="Signals selectbox")
                    if chosen_signal_index != 0 and st.session_state.Signals != [" "]:
                        frequency_value = st.session_state.Signals[chosen_signal_index-1]["Frequency"]
                        amplitude_value = st.session_state.Signals[chosen_signal_index-1]["Amplitude"]
                        edit_col1, edit_col2 = st.columns([1, 1])
                        with edit_col2:
                            new_amplitude_placeholder=st.empty()
                            new_amplitude = new_amplitude_placeholder.number_input("New Amplitude", min_value=1,max_value=1000,value=amplitude_value, step=1,key="amp_inp")
                            update_btn_placeholder=st.empty()
                            edit_signal_btn = update_btn_placeholder.button("Update Signal",key="update_btn")
                            if edit_signal_btn:
                                st.session_state.Signals[chosen_signal_index -1]["Frequency"] = st.session_state.freq_btn
                                st.session_state.Signals[chosen_signal_index -1]["Amplitude"] = new_amplitude
                        with edit_col1:
                            new_frequency_placeholder=st.empty()
                            new_frequency = new_frequency_placeholder.number_input("New Frequency", min_value=1,max_value=1000,value=frequency_value, step=1,key="freq_btn")
                            remove_btn_placeholder=st.empty()
                            remove_signal_btn =remove_btn_placeholder.button("Remove Signal",key="remove_btn")
                            if remove_signal_btn:
                                st.session_state.Signals.pop(chosen_signal_index-1)
                                labels_list.pop(chosen_signal_index)
                                selectbox_placeholder.selectbox("Choose Signal to edit", range(len(labels_list)), format_func=lambda x: labels_list[x],index=0)
                                new_frequency_placeholder.number_input("New Frequency", min_value=1,value=frequency_value, step=1,disabled=True)
                                remove_btn_placeholder.button("Remove Signal",disabled=True)
                                new_amplitude_placeholder.number_input("New Amplitude", min_value=1,value=amplitude_value, step=1,disabled=True)
                                update_btn_placeholder.button("Update Signal",disabled=True)
                else:
                    st.write("No signals are added ")
            with noise_addition:
                space_col,noise_checkbox_col,noise_slider_col = st.columns([0.1,0.8,3.5])
                with noise_checkbox_col:
                    st.subheader(" ")
                    noise_flag = st.checkbox("Add Noise to current Signal")
                with noise_slider_col:
                    noise_level = st.slider(
                        "Noise Level(SNR)", -100, 100, step=1, value=0, disabled=not noise_flag)

            with upload_signal:
                def new_upload():
                    st.session_state["uploaded_file_flag"] = True
                st.warning('Any New uploading file will reset your whole work!!', icon="⚠️")
                uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False, type=['json'], on_change=new_upload)
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

    with st.container():
        data_col, graphs_col = st.columns([1, 2], gap="medium")
        with data_col:
            st.header("Current Signals")
            if "Signals" in st.session_state:
                st.table(st.session_state.Signals)
                saved_data_structure = [
                    {"Noise_flag": noise_flag, "Noise_Value": noise_level, "Signals": st.session_state.Signals}]
                data_json_string = json.dumps(saved_data_structure)
                save_signals_btn = st.download_button(
                    label="Download Current Signal",
                    file_name="data.json",
                    mime="application/json",
                    data=data_json_string,
                )
            else:
                st.write("No Signals to display")
            sampling_frequency = 1
            h3 = '<h3 class="h3">Sampling & Reconstruction</h3>'
            st.markdown(h3,unsafe_allow_html= True)
            frequency_mode = st.selectbox(
                "Sample Rate(HZ)", ("Normailzed Frequency, 10Hz", "Normailzed Frequency, 100Hz","Normailzed Frequency, 500Hz","Fmax"))
            if frequency_mode == "Normailzed Frequency, 10Hz":
                start = 1
                end = 10
                sampling_frequency = st.slider(" ", label_visibility="hidden", min_value=start, max_value=end, disabled=empty_signals_flag)
            elif frequency_mode == "Normailzed Frequency, 100Hz":
                start = 1
                end = 100
                sampling_frequency = st.slider(" ", label_visibility="hidden", min_value=start, max_value=end, disabled=empty_signals_flag)
            elif frequency_mode == "Normailzed Frequency, 500Hz":
                start = 1
                end = 500
                sampling_frequency = st.slider(" ", label_visibility="hidden", min_value=start, max_value=end, disabled=empty_signals_flag)
            elif frequency_mode == "Fmax":
                start = 1.0
                end = 5.0
                s_value = st.slider(" ", label_visibility="hidden",min_value=start, max_value=end, disabled=empty_signals_flag)
                if empty_signals_flag:
                    sampling_frequency = 1
                else:
                    sampling_frequency = s_value * max_frequency
            time = st.slider("Time dispalyed (s)", 0.0, 5.0, step=0.1,value=1.0)
            reconstruct_flag = st.checkbox(" Show Reconstruction graph")

        with graphs_col:
            sinewave = np.zeros(500)
            time_axis = np.linspace(0, time, 500)
            if 'Signals' in st.session_state:
                for signal in st.session_state.Signals:
                    sinewave += signal["Amplitude"] * \
                        np.sin(2 * np.pi * signal["Frequency"] * time_axis)
                if noise_flag:
                    sinewave += helper.add_noise(noise_level)
                sampling_points = helper.sampling_func(
                    sampling_frequency, time_axis, sinewave, time)
            trace0 = go.Scatter(
                x=time_axis,
                y=sinewave,
                name='Signal'
            )
            trace1 = go.Scatter(
                x=sampling_points[0],
                y=sampling_points[1],
                mode='markers',
                name='Sample Points'
            )
            data = [trace0, trace1]
            layout = go.Layout(title="Signal With Sampling", xaxis={'title': 'Time'}, yaxis={'title': 'Amplitude'})
            fig = go.Figure(data=data, layout=layout)
            fig.update_layout(legend=dict(orientation= "h",yanchor="bottom",y=1.02,xanchor="right",x=1 ))

            st.plotly_chart(fig, use_container_width=True)
            if reconstruct_flag:
                trace2 = go.Scatter(
                    x=time_axis,
                    y=helper.reconstruction(time_axis, sampling_frequency, len(
                        sampling_points[0]), sampling_points[1]),
                    name="Reconstructed Points",
                    marker = {'color' : 'green'}
                )
                data = [trace2]
                layout = go.Layout(title="Reconstructed signal", xaxis={'title': 'Time'}, yaxis={'title': 'Amplitude'})
                fig = go.Figure(data=data, layout=layout)
                st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
