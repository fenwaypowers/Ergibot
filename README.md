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

* Role reaction monitor abilities.
* Simple commands for public use such as /wiki and /website.

## Code Structure

* `main.py` creates a cogs list to use the modules in `cogs/`.
* `utils.py` is for json loading and saving utils.
* `apikeys.py` is for loading api keys and server Ids.
* cog modules explained below.

## Admin.py

* For admin commands, such as `/botsay`.
* Full role monitoring and adding role monitors.
* Only users with the admin role (as specified in the cfg) can use these commands.

## Greetings.py

* For `on_member_update()` functionality.
* Gives the "Friends" role to new members who pass the rules screening.

## General.py

* For general public use functions such as retrieval of commonly used links.