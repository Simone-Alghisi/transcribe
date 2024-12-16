import argparse
import os
import shutil
import signal
import subprocess
import sys
import time
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from groq import Groq
from tqdm import tqdm


def signal_handler(sig, frame):
    shutil.rmtree(args.tmp_dir, ignore_errors=True)
    sys.exit(0)


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
        "--tmp-dir",
        "-tmp",
        metavar="TMP_DIR_PATH",
        type=str,
        default="tmp",
        help="Path to the directory where the temporary files will be saved.",
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


def transcribe_audio_file(tmp_file: str, args: Namespace, client: Groq) -> str:
    with open(str(tmp_file), "rb") as file:
        try:
            transcription = client.audio.transcriptions.create(
                file=(tmp_file, file.read()),  # Required audio file
                model=args.model,  # Required model to use for transcription
                language=args.language,  # Optional
            )
        except Exception as e:
            if e.status_code == 429:  # type: ignore
                wait_time = e.message.split("try again in ")[-1].split(". Visit")[0]  # type: ignore
                minutes, seconds = wait_time.split(".")
                seconds = seconds if len(seconds) < 7 else seconds[:6] + "s"
                wait_time = f"{minutes}.{seconds}"
                wait_time = datetime.strptime(wait_time, "%Mm%S.%fs")
                wait_time = wait_time.minute * 60 + wait_time.second + 2
                for _ in tqdm(range(wait_time), desc="Waiting"):
                    time.sleep(1)

                return transcribe_audio_file(tmp_file, args, client)
            else:
                print(e.status_code)  # type: ignore
                print(e.message)  # type: ignore

    return transcription.text


def main(args: Namespace, client: Groq) -> None:
    # create directories if they don't exist
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(args.tmp_dir, exist_ok=True)
    audio_files: List[Path] = [
        audio_file
        for file_type in ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
        for audio_file in Path(args.input_dir).rglob(f"*.{file_type}")
    ]

    for audio_file in tqdm(audio_files, desc="Transcribing audio files"):
        filename = audio_file.stem
        output_file = Path(args.output_dir) / f"{filename}.txt"

        if output_file.exists():
            print(f"Skipping {audio_file} as it has already been transcribed.")
            continue

        tmp_file = os.path.join(args.tmp_dir, f"{audio_file.stem}.mp3")
        # Convert the file using ffmpeg
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                audio_file,
                "-vn",  # disable video
                "-ac",
                "1",
                "-ar",
                "16000",
                tmp_file,
            ]
        )

        # Transcribe the converted file
        with open(tmp_file, "rb") as file:

            # Create a transcription of the audio file
            transcription = transcribe_audio_file(tmp_file, args, client)

            # Print the transcription text
            with open(output_file, "w") as f:
                f.write(transcription)

    # Remove the temporary file
    shutil.rmtree(args.tmp_dir)


# Remove tmp folder on SIGINT
signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    load_dotenv()
    assert os.getenv("GROQ_API_KEY"), "Please provide a GROQ_API_KEY in the .env file"
    args = get_args()

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    main(args, client)
