import streamlit as st
import tempfile
from video_audio import download_video, extract_audio
from model import classify_accent, MODEL_OPTIONS, load_accent_classifier
import scipy.io.wavfile as wav


st.title("Accent Classification Tool")

# Input fields
url = st.text_input("Video URL (MP4 or Loom):")
model_key = st.selectbox("Choose model:", list(MODEL_OPTIONS.keys()))

# New: time range slider (in seconds)
min_time, max_time = st.slider(
    label="Select time range (seconds)",
    min_value=0,
    max_value=160000,
    value=(5, 10),
    step=1
)

# New: TXT file uploader
txt_file = st.file_uploader("Upload your cookie file:", type="txt")


if st.button("Analyze Accent"):

    with st.spinner(f"Loading model '{model_key}'..."):
        try:
            st.session_state.classifier = load_accent_classifier(model_key)
            st.success(f"Model '{model_key}' loaded successfully.")
        except Exception as e:
            st.error(f"Error loading model: {e}")

    with st.spinner("Processing..."):

        try:
            # Work in a temporary directory for video and audio
            with tempfile.TemporaryDirectory() as tmpdir:
                video_file = download_video(url, tmpdir)
                wav_path = tmpdir + '/audio.wav'
                # Extract only the selected segment
                extract_audio(video_file, wav_path)#, start_time=min_time, end_time=max_time)

                # Read audio and slice by user-specified time range
                sample_rate, data = wav.read(wav_path)
                start_idx = int(min_time * sample_rate)
                end_idx = int(max_time * sample_rate)
                segment = data[start_idx:end_idx]
                # Write segment to a new WAV
                wav.write(wav_path, sample_rate, segment)

                label, confidence = classify_accent(wav_path, model_key,  st.session_state.classifier)

            st.success(f"Accent: {label} ({confidence:.2f}%)")
        except Exception as e:
            st.error(f"Error: {e}")
