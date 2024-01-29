import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.utils import get
import os
import utils
import aiohttp
import datetime
import globals
from database import *
from typing import Optional

class Database(commands.Cog):
    serverIdList = globals.config.servers.server_list

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name = "put", description = "Add an item to the database.", guild_ids=serverIdList)
    async def put(self, interaction: Interaction, key: str, entry: Optional[str], attachment: Optional[nextcord.Attachment], code_language: Optional[str], override: bool = False):
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

            if attachment:
                # User sent a file, save it to the filesystem
                local_path = f'db/{username}/{attachment.filename}'
                # Create the directory if it doesn't exist
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                await attachment.save(local_path)

                # Define the file extension
                file_extension = os.path.splitext(attachment.filename)[1]
                file_type = file_extension.lstrip('.')

                # Store the entry to the database
                conn = create_connection()
                store_entry(conn, (username, userid, date, attachment.url, key, file_extension, file_type, local_path, "file", code_language))
                select_all_links(conn)

                await interaction.response.send_message(f'Successfully stored `{key}`!')

            elif entry:
                if utils.is_url(entry):
                    # The entry is a link

                    # Define the file extension
                    file_type = entry.split("?")[0].split(".")[-1]
                    file_extension = "." + file_type

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
                    store_entry(conn, (username, userid, date, entry, key, file_extension, file_type, local_path, "link", code_language))
                    select_all_links(conn)

                elif code_language:
                    # The entry is a code snippet

                    # Store the entry to the database
                    conn = create_connection()
                    store_entry(conn, (username, userid, date, entry, key, None, None, None, "code", code_language))
                    select_all_links(conn)

                else:
                    # The entry is text

                    # Store the text entry to the database
                    conn = create_connection()
                    store_entry(conn, (username, userid, date, entry, key, None, None, None, "text", None))
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
                lang = row[row_dict["language"]]

                if entry_type == "link" or entry_type == "file":
                    local_path = row[row_dict["local_path"]]

                    # Check if link is valid
                    async with aiohttp.ClientSession() as session:
                        async with session.get(entry) as response:
                            if lang:
                                await interaction.response.send_message(file=nextcord.File(local_path))
                            elif response.status == 200:
                                await interaction.response.send_message(entry)
                            else:
                                await interaction.response.send_message("The original link is broken, but here is the archived file:")
                                await interaction.channel.send(file=nextcord.File(local_path))

                            if show_key:
                                await interaction.channel.send(f"Key: `{key}`\n")

                elif entry_type == "code":
                    # For text entries, simply send the stored text inside a markdown code block with the language identifier

                    await interaction.response.send_message(f"```{lang}\n{entry}\n```")
                    if show_key:
                        await interaction.channel.send(f"Key: `{key}`\n")

                elif entry_type == "text":
                    # For text entries, simply send the stored text
                    await interaction.response.send_message(entry)
                    if show_key:
                        await interaction.channel.send(f"Key: `{key}`\n")
        else:
            await interaction.response.send_message(f"No entries found for the provided key: `{key}`.")

        select_all_links(conn)
        close_connection(conn)

def setup(client):
    client.add_cog(Database(client))
