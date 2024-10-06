import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template for generating summary
prompt = """
You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing the most important points
within 250 words. Please provide the summary of the text given here: 
"""

# Extract the transcript from a YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Generate summary using Gemini API
def generate_gemini_content(transcript_text, prompt):
    try:
        # Call the `generate_text` method instead of using `GenerativeModel`
        response = genai.generate_text(
            model="models/text-bison-001",  # Adjust the model name as needed
            prompt=prompt + transcript_text,
            max_output_tokens=200  # Limit the output to 200 tokens (adjust as necessary)
        )

        # Extract the summary from the response
        if 'candidates' in response and len(response['candidates']) > 0:
            summary = response['candidates'][0]['output']
            return summary
        else:
            return "Error: No summary generated."

    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Streamlit application
st.title("YouTube Transcript to Detailed Notes Converter")

# Input for the YouTube link
youtube_link = st.text_input("Enter YouTube Video Link:")

# Show thumbnail of the YouTube video
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Button to fetch detailed notes
if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text and "Transcripts are disabled" not in transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
    elif "Transcripts are disabled" in transcript_text:
        st.error("Transcripts are disabled for this video.")
    else:
        st.error("Could not fetch transcript.")
