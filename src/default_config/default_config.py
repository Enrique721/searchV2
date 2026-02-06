from typing import TypedDict
import os

class Config(TypedDict):
    home: str
    default_db_file: str
    default_db_dir: str
    default_log_consume_dir: str
    default_log_not_processed_dir: str
    default_log_processed_dir: str


config: Config = {
    "home": os.path.expanduser("~"),
    "default_db_file": "smartHunter.db",
    "default_db_dir": os.path.join(os.path.expanduser("~"), ".local", "share", "smartHunter"),

    "default_log_consume_dir": os.path.join(os.path.expanduser("~"), "telegram", "consumeDir"),
    "default_log_not_processed_dir": os.path.join(os.path.expanduser("~"), "telegram", "notProcessed"),
    "default_log_processed_dir": os.path.join(os.path.expanduser("~"), "telegram", "processed"),
}

