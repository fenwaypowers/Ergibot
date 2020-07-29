'''Module for helper functions'''
import sys


def print_error(msg, module='core', stream=sys.stdout, **kwargs):
    '''Logs a message as an error'''
    print(f'[{module}/error] {msg}', file=stream, **kwargs)


def print_warn(msg, module='core', stream=sys.stdout, **kwargs):
    '''Logs a message as a warning'''
    print(f'[{module}/warn] {msg}', file=stream, **kwargs)


def print_info(msg, module='core', stream=sys.stdout, **kwargs):
    '''Logs a message as an info'''
    print(f'[{module}/info] {msg}', file=stream, **kwargs)


class NauticockError(Exception):
    '''Base exception for nauticock errors'''
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class PluginError(Exception):
    '''Base exception for errors within a plugin'''
    def __init__(self, name, msg):
        super().__init__(f'{name}: {msg}')
        self.msg = msg
        self.plugin_name = name
