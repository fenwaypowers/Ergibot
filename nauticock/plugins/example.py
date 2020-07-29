'''Basic example plugin that replys with the Nyx message from Persona 3'''
from discord.ext import commands

from .common import BasicPlugin

RESPONSE = ('The moment man devoured the fruit of knowledge, he sealed his '
            'fate... Entrusting his future to the cards, man clings to a dim '
            'hope. Yet, the Arcana is the means by which all is revealed. '
            'Beyond the beaten path lies the absolute end. It matters not who '
            'you are, Death awaits you.')


class ExamplePlugin(BasicPlugin):
    '''Example plugin. All plugins need to extend the BasicPlugin class'''

    # REQUIRED: unique id for your plugin. This is used for storage and logs
    plugin_name = 'example_plugin'
    # REQUIRED: Plugin API version. For now the only value is 0
    plugin_api_ver = 0

    # Do any config reads in here
    def __init__(self, bot):
        super().__init__(bot)
        test_dict = self.get_config_var('test_dict', {'stored': True})
        test_arr = self.get_config_var('test_arr', [1, 2, 3])

    # See https://discordpy.readthedocs.io/en/latest/api.html and
    # https://discordpy.readthedocs.io/en/latest/ext/commands/api.html for
    # event names
    @commands.Cog.listener()
    async def on_message(self, message):
        '''This is called on any message sent in discord by a user. Do not
        use this for commands! Use on_command instead
        '''

        # Don't get stuck in an infinite loop
        if message.author == self.bot.user:
            return

        if message.content.lower() == ('the arcana is the means by which all '
                                       'is revealed'):
            self.log_info('Request received, responding.')
            await message.channel.send(RESPONSE)
