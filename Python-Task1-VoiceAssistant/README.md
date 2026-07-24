# Task 1 - Voice Assistant

**Internship:** Oasis Infobyte - Python Programming Internship (OIBSIP)
**Intern:** Ammar Hassan

## Description
A desktop voice assistant built in Python that listens to spoken commands through the microphone, processes them, and responds using text-to-speech. It can tell the time and date, search Wikipedia, open websites, and perform Google searches — all through voice interaction.

## Features
- Voice input via microphone (Google Speech Recognition API)
- Text-to-speech responses (offline, using pyttsx3)
- Greets the user based on time of day
- Supported commands:
  - "What's the time" / "What's the date"
  - "Wikipedia [topic]" — reads a short summary
  - "Open YouTube" / "Open Google"
  - "Search for [query]"
  - "Who are you" / "What is your name"
  - "Stop" / "Exit" / "Quit" / "Goodbye" — ends the assistant

## Tech Stack
- Python 3
- `SpeechRecognition` — converts speech to text
- `pyttsx3` — offline text-to-speech engine
- `wikipedia` — fetches Wikipedia summaries
- `PyAudio` — microphone input handling

## Installation
```bash
pip install SpeechRecognition pyttsx3 wikipedia pywhatkit
pip install pipwin
python -m pipwin install pyaudio
```

## How to Run
1. Make sure your microphone is connected and working.
2. Open this folder in terminal.
3. Run:
   ```
   python voice_assistant.py
   ```
4. Wait for the greeting, then speak a command (e.g., "What's the time?").

## Status
Completed

---
*This project was completed as part of the AICTE Oasis Infobyte Internship Program.*
