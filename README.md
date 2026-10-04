# Personal Voice Assistant

A small Python assistant that recognizes spoken commands, matches them against explicit rules, and responds with speech. If speech dependencies or audio hardware are unavailable, it falls back to text input and output.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[voice]"
```

Speech recognition uses Google's web recognition service, so spoken commands need an internet connection. Microphone input additionally requires PyAudio; install it with `python -m pip install -e ".[microphone]"`. On Windows, PyAudio may require Microsoft C++ Build Tools to compile. The assistant remains usable in text mode if microphone setup fails.

## Run

```powershell
python -m personal_voice_assistant
```

## Sample commands

- `help` or `what can you do`
- `tell me the time`
- `search for weather today` or `google python tutorials`
- `open notepad`
- `open calculator`
- `exit`, `stop`, or `goodbye`

Only the listed applications can be launched. Web searches open in the default browser.

## Tests

```powershell
python -m unittest discover -s tests -v
```