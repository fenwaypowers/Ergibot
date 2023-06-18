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
from typing import Optional

class Database(commands.Cog):
    serverIdList = apikeys.serverIdList()

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "put", description = "Add an item to the database.", guild_ids=serverIdList)
    async def put(self, interaction: Interaction, key: str, entry: Optional[str], att: Optional[nextcord.Attachment], override: bool = False):
        # Obtain the user information
        username = interaction.user.name
        userid = str(interaction.user.id)

        conn = create_connection()

        rows = retrieve_link(conn, key)
        row_dict = get_row_index()

        do_override = False

        if rows and override:
            for row in rows:
                if row[row_dict["userid"]] == str(interaction.user.id):
                    do_override = True
                    # Delete the existing entry
                    delete_entry(conn, key)
                    break

        if not key_exists(conn, key) or do_override:

            # Obtain current date
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if att:
                # User sent a file, save it to the filesystem
                local_path = f'db/{username}/{att.filename}'
                await att.save(local_path)

                # Define the file extension
                file_extension = os.path.splitext(att.filename)[1]
                file_type = file_extension.lstrip('.')

                # Store the entry to the database
                conn = create_connection()
                store_entry(conn, (username, userid, date, att.url, key, file_extension, file_type, local_path, "file"))
                select_all_links(conn)

                await interaction.response.send_message(f'Successfully stored `{key}`!')
            elif entry:
                if utils.is_url(entry):  # Add a function to check if the entry is a URL
                    # The entry is a link
                    
                    # Define the file extension
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
                else:
                    # The entry is a text

                    # Store the text entry to the database
                    conn = create_connection()
                    store_entry(conn, (username, userid, date, entry, key, None, None, None, "text"))
                    select_all_links(conn)

                await interaction.response.send_message(f'Successfully stored `{key}`!')
            else:
                await interaction.response.send_message(f"No entry or file provided. Try again.")
        else:
            await interaction.response.send_message(f"Key: `{key}` already exists. Try a different key or use the override option.")
        
        close_connection(conn)

    @nextcord.slash_command(name = "get", description = "Retrieve an item from the database.", guild_ids=serverIdList)
    async def get(self, interaction: Interaction, key: str, show_key: bool = True):
        conn = create_connection()
        rows = retrieve_link(conn, key)
        row_dict = get_row_index()

        if rows:
            for row in rows:
                entry_type = row[row_dict["type"]]
                entry = row[row_dict["entry"]]
                
                if entry_type == "link" or entry_type == "file":
                    local_path = row[row_dict["local_path"]]
                    
                    # Check if link is valid
                    async with aiohttp.ClientSession() as session:
                        async with session.get(entry) as response:
                            if response.status == 200:
                                if show_key:
                                    await interaction.channel.send(f"Key: `{key}`\n")
                                await interaction.response.send_message(entry)
                            else:
                                await interaction.response.send_message("The original link is broken, but here is the archived file:")
                                await interaction.channel.send(file=nextcord.File(local_path))

                elif entry_type == "text":
                    # For text entries, simply send the stored text
                    if show_key:
                        await interaction.channel.send(f"Key: `{key}`\n")
                    await interaction.response.send_message(entry)
        else:
            await interaction.response.send_message(f"No entries found for the provided key: `{key}`.")
        
        select_all_links(conn)
        close_connection(conn)

def setup(client):
    client.add_cog(Database(client))
    