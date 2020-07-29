'''
Discord bot for the CIF discord. This package is fully pluggable and
should automatically load any properly designed package in the plugin
directory.

Jack Yu <yuydevel at protonmail dot com>
Summer 2020, Mid-COVID-19 pandemic
'''
import sys
import traceback

from discord.errors import LoginFailure, DiscordException

from .core import Nauticock
from .options import parse_args
from .utils import NauticockError, PluginError


def _main_core(args):
    argn = parse_args(args)
    settings = {}
    settings['storage-dir'] = argn.storage_dir
    settings['config-dir'] = argn.config_dir
    settings['api-key'] = argn.api_key
    try:
        with Nauticock(settings) as nauticock:
            nauticock.init_connection()
    except PluginError as err:
        trace = traceback.format_exc()
        sys.exit((f'ERROR: Plugin "{err.plugin_name}" has encountered an '
                  f'error\n{trace}'))
    except NauticockError:
        trace = traceback.format_exc()
        sys.exit(f'ERROR: A general error has occured\n{trace}')
    except LoginFailure:
        sys.exit('ERROR: Failed to login to discord, is the API key valid?')
    except DiscordException:
        trace = traceback.format_exc()
        sys.exit(f'ERROR: A discord error has occured\n{trace}')


def main(args):
    '''
    Wrapper around the real main function, checks the runtime and
    handles ctrl-c
    '''
    if sys.version_info <= (3, 6, 0):
        sys.exit('ERROR: Minimum Python version 3.6.0 required')
    try:
        _main_core(args)
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')


__all__ = ['main', 'Nauticock']
