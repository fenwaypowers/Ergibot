'''Module containing various classes that deal with json data storage'''
import os
import json
import traceback

from .utils import NauticockError, print_warn, print_info
from .reference import STORAGE_FILE_SUFFIX


def write_to_file(data, fpath):
    '''Writes data to filepath'''
    try:
        with open(fpath, 'w') as outfile:
            json.dump(data, outfile, indent=4)
    except OSError as err:
        raise NauticockError(f'Failed to write to file: "{fpath}"') from err


def read_from_file(fpath):
    '''Read data from filepath, returns None on fail'''
    try:
        with open(fpath, 'r') as outfile:
            data = json.load(outfile)
            return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        trace = traceback.format_exc()
        print_warn(f'Corrupted json file "{fpath}" found, skipping\n{trace}')
        return None
    except OSError as err:
        raise NauticockError(f'Failed to read from file: "{fpath}"') from err


class BaseStorage:
    '''Generic storage handler class'''
    def __init__(self, basepath):
        self.basepath = basepath
        self._dirty = []
        self._storagedict = {}
        try:
            os.makedirs(basepath, exist_ok=True)
        except OSError as err:
            raise NauticockError(f'Failed to create "{basepath}"') from err

    def load(self, namespace):
        '''Unwrapped lazy fetching of storage of a given namespace.
        You shouldn't be using this directly unless you are modifying the
        core framework.
        '''
        if namespace in self._storagedict.keys():
            return self._storagedict[namespace]
        fpath = os.path.join(
            self.basepath,
            f'{namespace}.{STORAGE_FILE_SUFFIX}')
        data = read_from_file(fpath)
        if data is None:
            data = {}
            self._dirty.append(namespace)
            print_info((f'Creating new file for "{fpath}". This will be saved '
                        'on the next call to flush()'))
        self._storagedict[namespace] = data
        return data

    def flush_all(self):
        '''Flushes any and all local changes to the filesystem.
        Try to avoid using this function as much as possible in plugins as
        simultanious namespace flushes from different plugins may have
        unintended effects. If possible, flush only your own plugin.
        Returns true if disk changes were made, false if otherwise
        '''
        if not self._dirty:
            return False
        curr = self._dirty.copy()
        self._dirty.clear()
        for namespace in curr:
            fpath = os.path.join(
                self.basepath,
                f'{namespace}.{STORAGE_FILE_SUFFIX}')
            write_to_file(self._storagedict[namespace], fpath)
        return True


class ConfigStorage(BaseStorage):
    '''Configuration storage handler class. Call Nauticock.config if needed'''

    def get(self, plugin, varname, default):
        '''Get a specified variable in a plugin's namespace'''
        namespace = f'p_{plugin}'
        conf = self.load(namespace)
        if varname not in conf:
            conf[varname] = default
            if namespace not in self._dirty:
                self._dirty.append(namespace)
        return conf[varname]


class DataStorage(BaseStorage):
    '''Configuration storage handler class. Call Nauticock.storage if needed'''
    def get(self, plugin, varname, default=None):
        '''Get a specified variable in a plugin's namespace'''
        namespace = f'p_{plugin}'
        data = self.load(namespace)
        if varname not in data:
            data[varname] = default
            if namespace not in self._dirty:
                self._dirty.append(namespace)
        return data[varname]

    def put(self, plugin, varname, value, always_dirty=True):
        '''Put a variable value in a plugin's namespace'''
        namespace = f'p_{plugin}'
        data = self.load(namespace)
        if not always_dirty and data[varname] is value:
            return False
        data[varname] = value
        if namespace not in self._dirty:
            self._dirty.append(namespace)
        return True

    def mark_dirty(self, plugin):
        '''Mark a plugin's namespace as dirty, which would force a save to
        disk on the next call to flush(). Returns true if the dirty state
        for the plugin changed, false if otherwise
        '''
        namespace = f'p_{plugin}'
        if namespace not in self._dirty \
                and namespace in self._storagedict.keys():
            self._dirty.append(namespace)
            return True
        return False

    def is_dirty(self, plugin=None):
        '''Checks whether a plugin is dirty, if none is specified, check
        if any namespace is dirty'''
        if plugin:
            return f'p_{plugin}' in self._dirty
        return bool(self._dirty)

    def flush(self, plugin):
        '''Flush the namespace of a given plugin to disk. Returns true if on
        disk changes were made, false if otherwise'''
        namespace = f'p_{plugin}'
        if namespace not in self._dirty:
            return False
        self._dirty.remove(namespace)
        fpath = os.path.join(
            self.basepath,
            f'{namespace}.{STORAGE_FILE_SUFFIX}')
        write_to_file(self._storagedict[namespace], fpath)
        return True
