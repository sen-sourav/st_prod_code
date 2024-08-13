import streamlit as st
from audiorecorder import audiorecorder
from app.model_loader import load_model
from app.model_inference import model_inference
import os
import pathlib

# Load model when Streamlit server starts
model = load_model()

def count_wav_files(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name)) and name.endswith('.wav')])

st.title("Add piano accompaniment")

input_file_dir = str(pathlib.Path("../uploads").resolve())
output_dir = str(pathlib.Path("../output").resolve())

audio = audiorecorder("Click to record", "Click to stop recording")
# Clear previous audio
st.empty()

if len(audio) > 0:

    # Generate new filename
    filename = f"audio_{(count_wav_files(input_file_dir))+1}.wav"
    input_file_path = f"{input_file_dir}/{filename}"
    out_audio_path = f'{output_dir}/{filename.split(".")[0]}_final_mix.wav'

    st.write(f"Input:")
    # To play audio in frontend:
    st.audio(audio.export().read())

    # To save audio to a file, use pydub export method:
    audio.export(input_file_path, format="wav")

    # To get audio properties, use pydub AudioSegment properties:
    #st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")

    # Perform model inference when user records sound
    model_inference(model, input_file_path, output_dir)
    
    st.write(f"Ouput:")
    st.audio(out_audio_path, format="wav", loop=False)


    # Display download buttons
    with open(input_file_path, "rb") as file:
        st.download_button("Download Original Audio", file, filename)

    with open(out_audio_path, "rb") as file:
        st.download_button("Download Processed Audio", file, out_audio_path.split("/")[-1])
