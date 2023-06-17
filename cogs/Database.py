import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
from nextcord.utils import get
import os, sys
import apikeys, utils
import aiohttp
import datetime
from database import *

class Database(commands.Cog):
    serverIdList = apikeys.serverIdList()

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "store", description = "Add an item to the database.", guild_ids=serverIdList)
    async def store(self, interaction: Interaction, key: str, entry: str):
        # Obtain the user information
        username = interaction.user.name
        userid = str(interaction.user.id)

        conn = create_connection()
        if not key_exists(conn, key):

            # Obtain current date
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if utils.is_url(entry):  # Add a function to check if the entry is a URL
                # The entry is a link

                # Find the file extension
                file_extension = os.path.splitext(entry)[1]
                file_type = file_extension.lstrip('.')
                
                # Define the local path for saving the file
                local_path = f'db/{username}/{key}{file_extension}'

                # Create user's directory if not exists
                if not os.path.exists(f'db/{username}'):
                    os.makedirs(f'db/{username}')
                
                # Download the file using aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(entry) as response:
                        if response.status == 200:
                            with open(local_path, 'wb') as f:
                                f.write(await response.read())

                # Store the entry to the database
                conn = create_connection()
                store_entry(conn, (username, userid, date, entry, key, file_extension, file_type, local_path, "link"))
                select_all_links(conn)
                close_connection(conn)
            else:
                # The entry is a text

                # Store the text entry to the database
                conn = create_connection()
                store_entry(conn, (username, userid, date, entry, key, None, None, None, "text"))
                select_all_links(conn)
                close_connection(conn)

            await interaction.response.send_message(f'Successfully stored {key}!')
        else:
            await interaction.response.send_message(f"Key: `{key}` already exists. Try a different key.")

    @nextcord.slash_command(name = "retrieve", description = "Retrieve an item from the database.", guild_ids=serverIdList)
    async def retrieve(self, interaction: Interaction, key: str):
        conn = create_connection()
        rows = retrieve_link(conn, key)
        row_dict = get_row_index()

        if rows:
            for row in rows:
                entry_type = row[row_dict["type"]]
                entry = row[row_dict["entry"]]
                
                if entry_type == "link":
                    local_path = row[row_dict["local_path"]]
                    
                    # Check if link is valid
                    async with aiohttp.ClientSession() as session:
                        async with session.get(entry) as response:
                            if response.status == 200:
                                await interaction.response.send_message(entry)
                            else:
                                await interaction.response.send_message("The original link is broken, but here is the archived file:")
                                await interaction.channel.send(file=nextcord.File(local_path))

                elif entry_type == "text":
                    # For text entries, simply send the stored text
                    await interaction.response.send_message(entry)
        else:
            await interaction.response.send_message("No entries found for the provided key.")
        
        select_all_links(conn)
        close_connection(conn)

def setup(client):
    client.add_cog(Database(client))
    