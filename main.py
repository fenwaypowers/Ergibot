import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
import os
import argparse
from config import load_config, Config
import globals

from config import Config

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
DEFAULT_CFG_PATH = os.path.join(SCRIPT_PATH, "config.cfg")

parser = argparse.ArgumentParser(description="Ergibot.")
parser.add_argument('--config', '-c', help='Path to ergibot config file.', default=DEFAULT_CFG_PATH)

args = parser.parse_args()
path_to_cfg = args.config
config: Config = load_config(path_to_cfg)
globals.config = config

serverIdList = config.servers.server_list
BOTTOKEN = config.api.key

intents = nextcord.Intents.all() # VITAL that this is .all()

client = commands.Bot(intents=intents)

initial_extensions = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(BOTTOKEN)
