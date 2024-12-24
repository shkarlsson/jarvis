# Jarvis

## Description

Jarvis is an attempt at a replacement for Google Home, Siri and Alexa but with genAI, better privacy and more control and customizability.

## Getting Started

### Installation

1. Clone the repository `git clone https://github.com/shkarlsson/jarvis.git`
2. Go to the repo `cd jarvis` 
3. Create a virtual environment and load it `python3.11 -m venv .venv && source .venv/bin/activate`. The version used by webrtcvad.py can't handle 3.12.
4. Install the dependencies `pip install -r requirements.txt`

### Configuration

1. Copy `config.env` and rename to `.env`
2. Get and add the required API keys to the `.env` file

### Running

1. Run `python -m main.app`

## Features

- [x] Wake word detection
- [x] Speech to text
- [x] Text to speech
- [x] Intent recognition

### Tools

- [x] Weather
- [x] Shopping list via Google Keep
- [ ] Web search
- [ ] News
- [ ] Music with Plex
- [/] Timer
- [ ] Zigbee control
- [ ] Public Transit

### QoL

- [ ] Selectable chimes

