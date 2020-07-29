'''
Module containing shared code for plugins
'''
from discord.ext.commands import Cog

from ..utils import print_warn, print_error, print_info
from ..reference import PLUGIN_API_VER


class BasicPlugin(Cog):
    '''An abstract plugin object'''
    plugins = {}

    def __init_subclass__(cls, abstract=False, **kwargs):
        '''Plugin auto-discovery part 1. This allows for imported
        plugin classes to automatically be loaded. To see the
        auto-discovery mechanism, see plugins/__init__.py
        '''
        super().__init_subclass__(**kwargs)
        if not abstract and isinstance(cls.plugin_name, str) \
                and cls.plugin_api_ver == PLUGIN_API_VER:
            cls.plugins[cls.plugin_name] = cls

    def __init__(self, bot):
        self.bot = bot

    @property
    def plugin_name(self):
        '''A unique string name of the plugin'''
        raise NotImplementedError('Abstract property not implemented')

    @property
    def plugin_api_ver(self):
        '''An int version for the plugin nauticock api, used to check for
        api version mismatches. Compare with PLUGIN_API_VER in reference.py
        '''
        raise NotImplementedError('Abstract property not implemented')

    def get_config_var(self, varname, default):
        '''Gets a value of a variable from the config file of the plugin. If
        the variable does not exist, it will be added to the config set to the
        specified default. The config store should not be set by the program
        and does not need to be flushed. For best practice, call this function
        in your plugin's __init__(). Only store primitives/dicts/lists.

        Default config is located in '$HOME/.config/nauticock' on Linux and
        '%APPDATA%\\Nauticock\\Config' on Windows

        varname: str - variable name to fetch
        default: any - default value if the variable is not found, will be
                       written to file on first run
        return: any - the stored data if found, default value otherwise
        '''
        return self.bot.config.get(self.plugin_name, varname, default)

    def get_storage_var(self, varname, default=None):
        '''Gets a value of a variable from the on-disk persistent storage of
        the plugin. Unlike the config version of this function. This can be
        called outside of __init__()

        Default storage is located in '$HOME/.cache/nauticock' on Linux and
        '%APPDATA%\\Nauticock\\Storage' on Windows

        varname: str - variable name to fetch
        default: any - default value of the var if not found. If set, will be
                       written to file if used (optional, default: None)
        return: any - the stored data if found, default value otherwise
        '''
        return self.bot.storage.get(self.plugin_name, varname, default=default)

    def put_storage_var(self, varname, value, always_dirty=True):
        '''Sets a variable on the storage of the plugin. For performance
        reasons, the value is not immediately written to disk. Nauticock will
        try to detect if changes were made in your plugin and will only write
        when needed (i.e flush_storage is called, or the program exits). Do
        note that this detect is not perfect, and if you modify elements
        within a dict/list, you would need to manually call
        mark_plugin_storage_dirty() so that it recognizes a write may be
        needed. To write to disk, call flush_storage().

        varname: str - variable name to modify
        value: any - the value to write. Only primitives, lists and dicts are
                     supported
        always_dirty: bool - advanced feature, normally any call to the
                             function sets the dirty flag. This is not best for
                             performance, but is the easiest. When set to false
                             Only when the reference value changes should the
                             dirty flag be set. Don't use this unless you are
                             sure what you are doing! (optional, default: True)
        return: bool - True if the plugin storage has become dirty, false if
                       otherwise
        '''
        return self.bot.storage.put(
            self.plugin_name,
            varname,
            value,
            always_dirty=always_dirty
        )

    def mark_plugin_storage_dirty(self):
        '''Manually marks the plugin storage as dirty (unsynced to disk). This
        would only be needed if a dict/list is modified directly. Any calls to
        put_storage_var on a primitive type should automatically do this. A
        plugin storage in a dirty state will automatically be written to disk
        on calls to flush_storage() or program exit.

        return: bool - True is returned if the dirty flag has changed, False
                      otherwise (plugin storage is already dirty)
        '''
        return self.bot.storage.mark_dirty(self.plugin_name)

    def flush_storage(self):
        '''Flushes any changes in saved data to disk, try to call this
        sparingly. This functionality is automatically done on program
        exit, so all you need to do is worry about potential crashes.
        Also, if you modify a dict/list directly, the storage handler
        would not know a change occured. Make sure to use
        mark_plugin_storage_dirty() to tell the handler that it needs
        to save stuff to file when available

        return: bool - True if disk content has changed, False if otherwise
        '''
        return self.bot.storage.flush(self.plugin_name)

    def log_warn(self, msg, **kwargs):
        '''Wrapper function for printing warning messages

        msg: str - message to output to log
        '''
        print_warn(msg, module=self.plugin_name, **kwargs)

    def log_info(self, msg, **kwargs):
        '''Wrapper function for printing info messages

        msg: str - message to output to log
        '''
        print_info(msg, module=self.plugin_name, **kwargs)

    def log_error(self, msg, **kwargs):
        '''Wrapper function for printing error messages

        msg: str - message to output to log
        '''
        print_error(msg, module=self.plugin_name, **kwargs)
