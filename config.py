from typing import Union, Set
import os
import configparser
import sys
from dataclasses import dataclass

@dataclass
class API:
    key: str

@dataclass
class Servers:
    server_list: Set[int]

@dataclass
class Admin:
    roles: Set[str]

@dataclass
class Config:
    api: API
    servers: Servers
    admin: Admin

def load_config(config_path: os.PathLike) -> Config:
    '''
    Load and validate the config file. Exits the program if the config is invalid.
    '''

    try:
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
    except Exception as e:
        print(f"Failed to load config file from {config_path}: {e}", file=sys.stderr)
        exit(1)

    try:
        api = API(key=cfg.get('api', 'key'))

        # Convert server_list to a set of integers
        server_list_str = cfg.get('servers', 'server_list').split(',')
        server_list_int = set()
        for server_id_str in server_list_str:
            try:
                server_id_int = int(server_id_str.strip())
                server_list_int.add(server_id_int)
            except ValueError:
                raise ValueError(f"Invalid server ID: {server_id_str}")
        servers = Servers(server_list=server_list_int)

        # Convert roles to a set of strings
        roles_str = cfg.get('admin', 'roles').split(',')
        roles_set = {role.strip() for role in roles_str}
        admin = Admin(roles=roles_set)

        config = Config(
            api=api,
            servers=servers,
            admin=admin
        )
    except Exception as e:
        print(f"Error in config file {config_path}: {e}", file=sys.stderr)
        exit(1)

    return config
