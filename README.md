# Ergibot

![Ergibot](https://cdn.discordapp.com/attachments/798075108853809163/1070183527368368158/a4e6e1caca365dd86bcfff7417fafac1.png)

Updated for 2024 with new slash commands, using [nextcord](https://github.com/nextcord/nextcord) for the API.

## Prerequisites:
* [Python >= 3.10.12](https://www.python.org/)

## Quick Start
- **(Recommended)** Create a virtual environment with `python3 -m venv .venv` and activate it with `source .venv/bin/activate`
- run `python3 -m pip install -r requirements.txt`
- copy `config.example.cfg` to `config.cfg` and adjust the configuration
- run `python3 main.py`

## Command Line Arguments
```
usage: main.py [-h] [--config CONFIG]

Ergibot.
        
options:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Path to ergibot config file.
```

## Features Implemented

* SQLite db for currency, files, text, and links
* Games: RPS and Blackjack
* Kevin and Joe commands
