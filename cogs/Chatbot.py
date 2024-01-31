import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import globals, chatbot

class Chatbot(commands.Cog):

    serverIdList = globals.config.servers.server_list
            
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="ask", description="Ask ergibot a question!", guild_ids=serverIdList)
    async def gatekeeper_log(self, interaction: Interaction, message: str, uncensored: bool = False):
        await interaction.response.defer()

        model = globals.config.chatbot.default_model
        if uncensored:
            model = globals.config.chatbot.alternate_model

        if globals.config.chatbot.type == 'local':
            bot = chatbot.LocalChatbot()
        elif globals.config.chatbot.type == 'server':
            bot = chatbot.ServerChatbot(user=interaction.user, msg=message)
        else:
            await interaction.followup.send("Chatbot incorrectly set up.")

        await interaction.followup.send(bot.get_reply(model))

def setup(client):
    client.add_cog(Chatbot(client))
