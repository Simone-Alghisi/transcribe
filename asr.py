import os
import argparse
from argparse import Namespace
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from groq import Groq
from tqdm import tqdm


def get_args() -> Namespace:
    """
    Parse command line arguments.

    Returns
    -------
    parsed_args: Namespace instance
        Parsed arguments passed through command line.
    """

    parser = argparse.ArgumentParser(
        prog="python -m generate_answers",
        description="Generate answers to questions using a model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--input-dir",
        "-in",
        metavar="INPUT_DIR_PATH",
        type=str,
        default="input",
        help="Path to the directory containing the input files to be trascribed.",
    )
    parser.add_argument(
        "--output-dir",
        "-out",
        metavar="OUTPUT_DIR_PATH",
        type=str,
        default="output",
        help="Path to the directory where the transcriptions will be saved.",
    )
    parser.add_argument(
        "--model",
        "-m",
        metavar="MODEL_NAME",
        type=str,
        choices=["whisper-large-v3-turbo", "whisper-large-v3"],
        default="whisper-large-v3-turbo",
        help="Model to use for transcription.",
    )
    parser.add_argument(
        "--language",
        "-l",
        metavar="LANGUAGE",
        type=str,
        default="it",
        help="Language of the audio file.",
    )

    args = parser.parse_args()

    return args


def main(args: Namespace, client: Groq) -> None:
    # Specify the path to the audio file
    filename = (
        os.path.dirname(__file__) + "/input/sample_audio.mp4"
    )  # Replace with your audio file!

    audio_files: List[Path] = [
        audio_file
        for file_type in ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
        for audio_file in Path(args.input_dir).rglob(f"*.{file_type}")
    ]

    for audio_file in tqdm(audio_files, desc="Transcribing audio files"):
        # Open the audio file
        with open(str(audio_file), "rb") as file:
            # Create a transcription of the audio file
            transcription = client.audio.transcriptions.create(
                file=(filename, file.read()),  # Required audio file
                model=args.model,  # Required model to use for transcription
                language=args.language,  # Optional
            )
            # Print the transcription text
            with open("transcription.txt", "w") as f:
                f.write(transcription.text)


if __name__ == "__main__":
    load_dotenv()
    assert os.getenv("GROQ_API_KEY"), "Please provide a GROQ_API_KEY in the .env file"
    args = get_args()

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    main(args, client)
