'''
Commandline argument parser module
Keep it simple, this isn't inkweaver
Plugin specific arguments should in the respective plugins
'''
from argparse import ArgumentParser

from .reference import (
    VERSION,
    PKGNAME,
    DEFAULT_CONFIG_PATH,
    DEFAULT_STORAGE_PATH
)


def parse_args(args):
    '''Parses arguments as program parameters and returns the result.
    This method will print usage and exit if invalid or no parameters
    are detected
    '''
    parser = ArgumentParser(
        prog=PKGNAME,
        description='pluggable CIF Discord channel manager bot'
    )
    parser.add_argument('-v', '--version', action='version',
                        version=(f'{PKGNAME} build {VERSION}. '
                                 'Designed by Jack Yu '
                                 '<yuydevel at protonmail dot com>'))
    parser.add_argument('-s', '--storage-dir', action='store',
                        metavar='location',
                        help=f'storage directory for persistent data. \
                        Default is set to "{DEFAULT_STORAGE_PATH}"')
    parser.add_argument('-c', '--config-dir', action='store',
                        metavar='location',
                        help=f'config directory for module. Default \
                        is set to "{DEFAULT_CONFIG_PATH}"')
    parser.add_argument('-t', '--api-key', action='store',
                        metavar='token',
                        help='API token required by discord. Setting \
                        this overrides the token specified in the config')

    options = parser.parse_args(args)
    return options
