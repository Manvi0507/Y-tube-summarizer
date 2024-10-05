import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re

load_dotenv()  # Load all the environment variables

# Configure Google Gemini with the API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key is missing. Please set it in the .env file.")
else:
    genai.configure(api_key=api_key)

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

# Extract video ID using regex
def extract_video_id(youtube_video_url):
    match = re.search(r"(?<=v=)[^&]+|(?<=be/)[^&]+", youtube_video_url)
    return match.group(0) if match else None

# Get the transcript from YouTube
def extract_transcript_details(video_id):
    try:
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([i["text"] for i in transcript_text])
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

# Generate summary content
def generate_gemini_content(transcript_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text if response else "No response from the model."

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    else:
        st.error("Invalid YouTube link. Please check and try again.")

if st.button("Get Detailed Notes"):
    if video_id:
        transcript_text = extract_transcript_details(video_id)

        if transcript_text:
            summary = generate_gemini_content(transcript_text)
            st.markdown("## Detailed Notes:")
            st.write(summary)
