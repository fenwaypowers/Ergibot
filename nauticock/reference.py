'''
Package-level static constants
'''
import os

# Increment on update
VERSION = 1
PKGNAME = 'nauticock'

# Change this when modifying how plugins are handled
PLUGIN_API_VER = 0

if os.name == 'nt':
    DEFAULT_STORAGE_PATH = os.path.expandvars('%APPDATA%\\Nauticock\\Storage')
    DEFAULT_CONFIG_PATH = os.path.expandvars('%APPDATA%\\Nauticock\\Config')
else:
    DEFAULT_STORAGE_PATH = os.path.expandvars('${HOME}/.cache/nauticock')
    DEFAULT_CONFIG_PATH = os.path.expandvars('${HOME}/.config/nauticock')

STORAGE_FILE_SUFFIX = 'json'

COMMAND_PREFIX = '/'
