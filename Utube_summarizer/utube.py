import streamlit as st
import io
from pytube import YouTube
import torch
from transformers import pipeline

# Load the Whisper model
@st.cache_resource
def load_whisper_model():
    model = pipeline("automatic-speech-recognition", model="openai/whisper-large")
    return model

# Function to download audio from YouTube and return as a BytesIO object
def download_audio(youtube_url):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = audio_stream.download(filename="audio.mp4")
    return audio_file

# Streamlit UI
st.title("YouTube Audio Transcriber and Summarizer with Whisper")

youtube_url = st.text_input("Enter YouTube Video URL:")

if st.button("Transcribe and Summarize"):
    if youtube_url:
        with st.spinner("Downloading audio..."):
            audio_file_path = download_audio(youtube_url)
        
        st.success("Audio downloaded successfully!")

        # Load the Whisper model
        whisper_model = load_whisper_model()

        with st.spinner("Transcribing audio..."):
            audio_bytes = io.BytesIO(audio_file_path)
            transcript = whisper_model(audio_bytes)["text"]
            st.success("Transcription completed!")
            st.write(transcript)

            with st.spinner("Summarizing text..."):
                summarizer = pipeline("summarization")
                summary = summarizer(transcript, max_length=130, min_length=30, do_sample=False)
                st.success("Summarization completed!")
                st.write(summary[0]['summary_text'])
    else:
        st.warning("Please enter a valid YouTube URL.")
