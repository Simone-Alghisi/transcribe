<!-- omit from toc -->
# Transcribe
A simple repository to transcribe video/audio using [Groq](https://groq.com). It also handles the `429 Too Many Requests` error when the quota is reached and automatically re-tries after the specified amount of time.


- [Installation](#installation)
  - [Python](#python)
  - [Python Environment](#python-environment)
  - [FFMPEG (Recommended)](#ffmpeg-recommended)
  - [Groq API](#groq-api)
- [Running the script](#running-the-script)
- [License](#license)



## Installation
This part will guide you through the installation of the mandatory components to run the script.


### Python
You can download Python Installer for your OS from its [official website](https://www.python.org/downloads/).


### Python Environment
First, create a Python environment in the script working directory by opening a terminal (or PowerShell on Windows) and running following command:

```shell
python -m venv transcribe
```

Then, you can activate the environment on Windows (PowerShell) using:

```shell
source transcribe\Scripts\Activate.ps1
```
> [!TIP]
> You can find more information about how to activate venv on other terminals/OS [here](https://docs.python.org/3/library/venv.html#how-venvs-work).

Once the environment has been activated, you can install the required packages by running the following command:

```shell
pip install -r requirements.txt
```


### FFMPEG (Recommended)
You can download FFmpeg for your current OS (Windows, Mac, or Linux) from [here](www.ffmpeg.org/download.html).

> [!IMPORTANT] 
> Although FFmpeg is not required for transcribing video/audio, it is recommended by Groq as written in the [documentation](https://console.groq.com/docs/speech-text):
>
> *Our speech-to-text models will downsample audio to 16,000 Hz mono before transcribing. This preprocessing can be performed client-side to reduce file size and allow longer files to be uploaded to Groq*.


### Groq API
Before running the script, you will need a set of API keys from Groq.

After creating your account on Groq, 
1. go to your [Developer Console](https://console.groq.com/keys) 
2. click on the `Create API key` Button
3. choose a name (e.g., transcribe)
4. copy the generated API key

> [!CAUTION]
> You cannot view your key afterwards, so be sure to copy it!
> 
> *However, if you mess up you can always delete the current key and generate a new one.*

At this point you must:
1. open the [`test.env`](./test.env) file (inside this script folder)
2. paste your newly generate API key after `GROQ_API_KEY=`
3. save the file, close it, and rename it as `.env`

> [!CAUTION]
> Changing the file name to `.env` also prevents you from inadvertedly pushing the API key to GitHub. 

## Running the script

After completing the installation, you can activate the environment (example provided in the [previous section](./README.md#python-environment)) and run the following:

```bash
python -m asr
```

The program will transcribe each file in the [`input`](./input) folder and place its transcription into the [`output`](./output) folder. Files that have already been transcribed will not be transcribed again.

You can take a look at the full list of arguments by adding `--help` to the previous command.

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This work is licensed under a [MIT License](https://opensource.org/licenses/MIT).