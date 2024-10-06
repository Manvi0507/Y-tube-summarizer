import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_transcript(video_id):
    """
    Fetch the transcript of a YouTube video.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item['text'] for item in transcript])
        return full_text
    except Exception as e:
        return str(e)

def summarize_text(text):
    """
    Summarize the text using the Gemini API.
    """
    try:
        # Use the 'chat' or 'generate_text' method depending on what Gemini supports
        response = genai.chat(
            model="gemini-1.5-pro",
            messages=[
                {"role": "system", "content": "Summarize the following text:"},
                {"role": "user", "content": text}
            ]
        )
        
        # Check if the 'candidates' list exists and has at least one item
        if 'candidates' in response and len(response['candidates']) > 0:
            summary = response['candidates'][0]['message']['content']
            return summary
        else:
            return "Error: No summary generated. Response did not contain valid candidates."

    except Exception as e:
        return f"Error generating summary: {str(e)}"

def extract_video_id(youtube_url):
    """
    Extract the video ID from a YouTube URL.
    """
    try:
        if "youtube.com" in youtube_url:
            return youtube_url.split("v=")[1]
        elif "youtu.be" in youtube_url:
            return youtube_url.split("/")[-1]
        else:
            return None
    except Exception as e:
        return None

def main():
    st.title("YouTube Video Transcript Summarizer (Gemini API)")

    # Input YouTube URL
    youtube_url = st.text_input("Enter YouTube Video URL:")
    
    if youtube_url:
        video_id = extract_video_id(youtube_url)
        if video_id:
            st.write("Fetching transcript...")
            transcript = get_transcript(video_id)
            
            if transcript:
                st.write("Transcript fetched. Generating summary...")
                summary = summarize_text(transcript)
                st.subheader("Summary:")
                st.write(summary)
            else:
                st.error("Could not retrieve transcript.")
        else:
            st.error("Invalid YouTube URL.")
    else:
        st.write("Please enter a YouTube video URL to get started.")

if __name__ == "__main__":
    main()
