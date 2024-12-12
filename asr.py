import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Specify the path to the audio file
filename = (
    os.path.dirname(__file__) + "/input/sample_audio.mp4"
)  # Replace with your audio file!

# Open the audio file
with open(filename, "rb") as file:
    # Create a transcription of the audio file
    transcription = client.audio.transcriptions.create(
        file=(filename, file.read()),  # Required audio file
        model="whisper-large-v3-turbo",  # Required model to use for transcription
        response_format="json",  # Optional
        language="it",  # Optional
        temperature=0.0,  # Optional
    )
    # Print the transcription text
    with open("transcription.txt", "w") as f:
        f.write(transcription.text)
