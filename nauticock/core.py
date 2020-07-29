'''Core module for Nauticock plugin framework'''
import signal

from discord.ext.commands import Bot

from .storage import ConfigStorage, DataStorage
from .plugins import init_plugins
from .reference import (
    COMMAND_PREFIX,
    DEFAULT_CONFIG_PATH,
    DEFAULT_STORAGE_PATH
)
from .utils import print_info


class Nauticock(Bot):
    '''Core class for Nauticock bot framework'''
    def __init__(self, init_params):
        super().__init__(COMMAND_PREFIX)
        print_info('Starting program')
        if not init_params['config-dir']:
            init_params['config-dir'] = DEFAULT_CONFIG_PATH
        print_info('Initializing config storage')
        self.config = ConfigStorage(init_params['config-dir'])

        core_conf = self.config.load('core')
        for key, value in [
                ['api-key', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'],
                ['storage-dir', DEFAULT_STORAGE_PATH]]:
            if key not in core_conf.keys():
                core_conf[key] = value
                if 'core' not in self.config._dirty:
                    self.config._dirty.append('core')

        if not init_params['storage-dir']:
            init_params['storage-dir'] = core_conf['storage-dir']
        if not init_params['api-key']:
            init_params['api-key'] = core_conf['api-key']
        print_info('Initializing storage space')
        self.storage = DataStorage(init_params['storage-dir'])

        print_info('Initializing plugins')
        init_plugins(self)
        self.init_params = init_params
        self.config.flush_all()

        def on_sig(self):
            print_info(('Writing changes to disk.'))
            self.config.flush_all()
            self.storage.flush_all()

        try:
            self.loop.add_signal_handler(signal.SIGINT, on_sig)
            self.loop.add_signal_handler(signal.SIGTERM, on_sig)
        except NotImplementedError:
            pass

        @self.event
        async def on_ready():
            print_info('Discord login successful')

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        print('')
        print_info(('Writing changes to disk.'))
        self.config.flush_all()
        self.storage.flush_all()
        return False

    def init_connection(self):
        '''Initializes the connection to discord and starts the program'''
        self.run(self.init_params['api-key'])
