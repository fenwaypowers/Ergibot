import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
import os, sys
import apikeys

if os.path.exists('keys/discord.txt') == False or os.path.exists('keys/serverids.txt') == False:
    print('''Please initialize the keys/ directory with discord.txt and serverids.txt.
    Put your Discord API key into discord.txt.
    Put the ID of the servers you want to allow the bot to message in.
    Therefore, you should have these files:
        keys/discord.txt
        keys/serverids.txt''')
    sys.exit(1)
else:
    print("Running Nauticock Bot...")

serverIdList = apikeys.serverIdList()
BOTTOKEN = apikeys.discordApiKey()

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