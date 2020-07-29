NauticockBot
============

NauticockBot is CIF's pluggable Discord bot framework, serving as a
boilerplate to simplify adding features to CIF's Discord server. This
project uses the 'discord.py[voice]' library with custom support for
config files and persistent data storage.

## Usage

```
usage: nauticock [-h] [-v] [-s location] [-c location] [-t token]

optional arguments:
  -v, --version         show program's version number and exit
  -s location, --storage-dir location
                        storage directory for persistent data.
  -c location, --config-dir location
                        config directory for module.
  -t token, --api-key token
                        API token required by discord. Setting this overrides
                        the token specified in the config
```

Configs are by default stored in `$HOME/.config/nauticock` for Unix and
`%APPDATA%\Nauticock\Config` for Windows. Persistent storage is located in
`$HOME/.cache/nauticock` for Unix and `%APPDATA%\Nauticock\Storage` for Windows
by default (this can be changed in core.json in the config folder).

A token is required to connect to the Discord servers. This can be either
specified at runtime or in the config file.


## Compiling to single binary

While the program can be directly invoked via `python3 -m nauticock`, you
can also compile the program into a single python binary. To do this, run
`make build`, the binary should be created in the `build` directory.

## Plugin development

To set up your development environment, install all dependencies in
`requirements.txt` in your favorite python management tool.

To write a plugin for Nauticock, create a new file in `nauticock/plugins`.
This file needs to have a class extend the 'nauticock.common.BasePlugin'
object for the autoloader to recognize the plugin. Your plugin object can
call any of the functions specified in `BasePlugin`, as well as use any
function that works with 'discord.ext.commands.Cog'. See the
[discord.py](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html)
documentation for more details.

Some provided utilty functions in `BasePlugin` are:

- `log_info`, `log_warn`, `log_error`
- `get_config_var`
- `get_storage_var`, `put_storage_var`, `mark_plugin_storage_dirty`, `flush_storage`

If your plugin is larger than a single file, you may want to write the whole
thing in a separate external module then import it. Feel free to ask for help
on the [CIF discord](https://discord.gg/TMKXqJc).

## License

This project is licensed under the LGPLv3. If you have any questions,
please contact the original author Jack Yu \<yuydevel at protonmail dot
com\>.
