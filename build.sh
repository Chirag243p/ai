#!/bin/bash

# Install PortAudio
apt-get update && apt-get install -y portaudio19-dev

# Install the Python dependencies
pip install -r requirements.txt
