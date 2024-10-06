import streamlit as st
import os
from pytube import YouTube
from pydub import AudioSegment
import speech_recognition as sr
from transformers import pipeline

# Function to download audio from YouTube
def download_audio(youtube_url):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file_path = audio_stream.download(filename="audio.mp4")
    return audio_file_path

# Function to convert audio to text
def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file_path, format="mp4")
    audio.export("audio.wav", format="wav")  # Convert to wav for recognition
    with sr.AudioFile("audio.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Function to summarize text
def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Streamlit UI
st.title("YouTube Audio Extractor and Summarizer")

youtube_url = st.text_input("Enter YouTube Video URL:")

if st.button("Extract and Summarize"):
    if youtube_url:
        with st.spinner("Downloading audio..."):
            audio_path = download_audio(youtube_url)
        
        st.success("Audio downloaded successfully!")

        with st.spinner("Transcribing audio..."):
            try:
                transcript = audio_to_text(audio_path)
                st.success("Transcription completed!")
                st.write(transcript)

                with st.spinner("Summarizing text..."):
                    summary = summarize_text(transcript)
                    st.success("Summarization completed!")
                    st.write(summary)
            except Exception as e:
                st.error(f"Error during transcription: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")

# Clean up temporary files
if os.path.exists("audio.mp4"):
    os.remove("audio.mp4")
if os.path.exists("audio.wav"):
    os.remove("audio.wav")
