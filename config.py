import os
import configparser
import sys
import logging
from dataclasses import dataclass
from typing import Set

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
class Chatbot:
    enabled: bool
    type: str
    command: str
    default_model: str
    alternate_model: str
    ip: str
    username: str
    password: str

@dataclass
class Config:
    api: API
    servers: Servers
    admin: Admin
    chatbot: Chatbot

def load_config(config_path: os.PathLike) -> Config:
    '''
    Load and validate the config file. Exits the program if the config is invalid.
    '''

    logging.basicConfig(level=logging.ERROR)

    try:
        cfg = configparser.ConfigParser()
        cfg.read(config_path)
    except Exception as e:
        logging.error(f"Failed to load config file from {config_path}: {e}")
        sys.exit(1)

    try:
        # API
        api_key = os.getenv('BOT_API_KEY', cfg.get('api', 'key'))
        api = API(key=api_key)

        # Servers
        server_list_str = cfg.get('servers', 'server_list').split(',')
        server_list_int = {int(server_id.strip()) for server_id in server_list_str}
        servers = Servers(server_list=server_list_int)

        # Admin
        roles_str = cfg.get('admin', 'roles').split(',')
        roles_set = {role.strip() for role in roles_str}
        admin = Admin(roles=roles_set)

        # Chatbot
        chatbot = Chatbot(
            enabled=cfg.getboolean('chatbot', 'enabled'),
            type=cfg.get('chatbot', 'type'),
            command=cfg.get('chatbot', 'command'),
            default_model=cfg.get('chatbot', 'default_model'),
            alternate_model=cfg.get('chatbot', 'alternate_model'),
            ip=cfg.get('chatbot', 'ip'),
            username=cfg.get('chatbot', 'username'),
            password=cfg.get('chatbot', 'password')
        )

        config = Config(
            api=api,
            servers=servers,
            admin=admin,
            chatbot=chatbot
        )
    except Exception as e:
        logging.error(f"Error in config file {config_path}: {e}")
        sys.exit(1)

    return config
