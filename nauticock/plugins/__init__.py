'''
Module containing all plugins to be loaded. Each plugin should be
self-contained in its own submodule. This allows for easy update of
plugins and easy debugging
'''
import importlib
import pkgutil

from .common import BasicPlugin
from ..utils import PluginError, print_info

_loaded_plugins = []


def init_plugins(bot):
    '''Plugin auto-discovery part 2. This imports all submodules in the
    plugin module so that the autoloader can load the classes. This
    method then attempts to initialize the plugins, completing the
    loading process
    '''
    if _loaded_plugins:
        return
    for _, name, _ in pkgutil.walk_packages(__path__):
        importlib.import_module(f'{__name__}.{name}')

    for name, cls in BasicPlugin.plugins.items():
        try:
            print_info(f'Loading plugin "{name}"')
            cog = cls(bot)
            _loaded_plugins.append(cog.plugin_name)
            bot.add_cog(cog)
        except Exception as err:
            raise PluginError(cls.plugin_name,
                              'failed to initialize plugin') from err


def get_loaded_plugins():
    '''Gets the list of currently loaded plugin names'''
    return _loaded_plugins
