import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt
prompt = """
You are a YouTube video summarizer. You will take the transcript text and summarize the entire video,
providing the important points in 250 words. Please provide the summary of the text given here:
"""

# Function to extract the video ID from a YouTube URL
def get_video_id(youtube_url):
    try:
        query = urlparse(youtube_url).query
        video_id = parse_qs(query).get("v")
        if video_id:
            return video_id[0]
        else:
            raise ValueError("Invalid YouTube URL format.")
    except Exception as e:
        raise ValueError("Failed to extract video ID. Please check the URL.") from e

# Function to extract transcript from a YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = get_video_id(youtube_video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript

    except Exception as e:
        raise e

# Function to generate summary using Gemini API
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        raise Exception("Failed to generate summary.") from e

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")

# Get YouTube link from user
youtube_link = st.text_input("Enter YouTube Video Link:")

# Display YouTube thumbnail if a link is provided
if youtube_link:
    try:
        video_id = get_video_id(youtube_link)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except ValueError as e:
        st.error(str(e))

# Button to generate notes
if st.button("Get Detailed Notes"):
    try:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
        else:
            st.warning("No transcript available for this video.")
    except Exception as e:
        st.error(str(e))
