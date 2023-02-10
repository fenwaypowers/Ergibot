import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ext import application_checks
import os, sys
import apikeys, utils, validators, requests, urllib
from pymediainfo import MediaInfo
import subprocess

from datetime import date
from datetime import datetime
from datetime import timedelta

from pytz import timezone

tz = timezone('EST')

class Database(commands.Cog):

    serverIdList = apikeys.serverIdList()
            
    def __init__(self, client):
        self.client = client

        self.path_to_db = "./db/"
        self.json_filename = "./db/db.json"

        if os.path.exists(self.path_to_db) == False:
            os.mkdir(self.path_to_db)

        if os.path.exists(self.json_filename) == False:
            f = open(self.json_filename, 'a')
            f.write("{\"entry\": {} }")
            f.close()
        
        self.db = utils.load_json(self.json_filename)
    
    @nextcord.slash_command(name="get", description="Retrieve an entry from the database", guild_ids=serverIdList)
    async def get(self, interaction: Interaction, key:str):
        await interaction.response.defer()

        if key in self.db["entry"]:
            filename = self.path_to_db + key + \
                self.db["entry"][key]["extension"]

            video_type = "none"

            if os.path.exists(filename):
                media_info = MediaInfo.parse(filename)
                for track in media_info.tracks:
                    if track.track_type == "Video":
                        if video_type == "none":
                            video_type = track.format
            
            if video_type == "AV1":
                
                continue_ = False

                embed = utils.Embedder.fromnothing()

                if embed.domain in self.db["entry"][key]["link"]:
                    embed = utils.Embedder.fromlink(
                        self.db["entry"][key]["link"])
                    r = requests.get(embed.img)
                    if r.status_code != 200:
                        continue_ = True
                else:
                    continue_ = True

                if continue_: #this will run if there is no embed link, or the 0x0 image is no longer on 0x0.
                    subprocess.run("ffmpeg -y -i " + filename + " -vf \"select=eq(n\, 0)\" -q:v 3 ./.temp/" + key + ".jpg", shell=True)
                    # extract first frame of the video

                    subprocess.run("curl -F \"file=@./.temp/" + key + ".jpg" + "\" 0x0.st > ./.temp/" + key + ".txt", shell=True)
                    # upload that frame to 0x0.st

                    image_link = "ERROR"

                    try:
                        with open("./.temp/" + key + ".txt") as image_link_file:
                            image_link = image_link_file.readlines()[0]
                    except:
                        pass

                    self.db["entry"][key]["link"] = str(utils.Embedder(
                        self.db["entry"][key]["link"], image_link)).rstrip()

                    self.db = utils.save_and_load_json(self.json_filename, self.db)

                    os.remove("./.temp/" + key + ".jpg")
                    os.remove("./.temp/" + key + ".txt")

            send_file = False
            if os.path.exists(filename):
                if os.path.getsize(filename) <= 8000000:
                    send_file = True
            
            if send_file:
                await interaction.followup.send(files=[nextcord.File(filename)])
            else:
                link = self.db["entry"][key]["link"]
                request = requests.get(link)

                if request.status_code == 200:
                    await interaction.followup.send(link)
                else:
                    await interaction.followup.send("That link has died \:(\nError code: " + str(request.status_code))
        else:
            await interaction.followup.send("No such entry found for key: `" + key + "`")

    @nextcord.slash_command(name="put", description="Enter data into the database", guild_ids=serverIdList)
    async def put(self, interaction: Interaction, key: str, link: str):
        await interaction.response.defer()
        user = interaction.user
        date = datetime.now(tz)
        
        if key in self.db["entry"]:
            await interaction.followup.send("The key: `" + key + "` is already in the database.")
        else:
            r = requests.get(link)
            if r.status_code != 200:
                await interaction.followup.send("Not a valid link.")
            else:
                self.db["entry"][key] = {"user": str(user), "userid": str(user.id), "date": str(date), "link": link, "extension": "." + link.split(".")[-1]}
                self.db = utils.save_and_load_json(self.json_filename, self.db)
                await interaction.followup.send("Key: `" + key + "` successfully saved to the database.")

        



def setup(client):
    client.add_cog(Database(client))