from typing import TypedDict
import os

log_consumption_directory = "consumeDir"
log_failed_consumption_directory = "notProcessed"
log_process_directory = "processed"

class Config(TypedDict):
    home: str
    default_db_file: str
    default_db_dir: str
    default_log_consume_dir: str
    default_log_not_processed_dir: str
    default_log_processed_dir: str

home_dir = os.path.expanduser("~")

config: Config = {
    "home": os.path.expanduser("~"),
    "default_db_file": "smartHunter.db",
    "default_db_dir": os.path.join(home_dir, ".local", "share", "smartHunter"),

    "default_log_consume_dir": os.path.join(home_dir, "telegram", log_consumption_directory),
    "default_log_not_processed_dir": os.path.join(home_dir, "telegram", log_failed_consumption_directory),
    "default_log_processed_dir": os.path.join(home_dir, "telegram", log_process_directory),
}

