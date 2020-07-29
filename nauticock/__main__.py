#!/usr/bin/env python3
'''
Entry point for the package. When compiled into a binary, this file is
moved outside of the package into the base directory
'''

import sys

# Check native dependencies
try:
    pass
except ModuleNotFoundError as err:
    sys.exit(f'ERROR: Missing dependency detected: {err.name}')

# direct call of __main__.py
if __package__ is None and not hasattr(sys, 'frozen'):
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import nauticock

if __name__ == '__main__':
    nauticock.main(sys.argv[1:])
