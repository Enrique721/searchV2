from src.parser.parser import Parser
from src.export.formatter import make_directory
from src.file_ops.file_operation import make_file_iterator
from src.default_config.default_config import config
from typing import Optional
import os
from pathlib import Path


def check_default_db_directory() -> bool:
    path_exists = Path(config["default_db_dir"]).exists()

    if path_exists:
        print("Diretório padrão encontrado")
    else:
        print("Diretório padrão não encontrado")

    return path_exists

def check_and_create_default_dir() -> bool:
    if not check_default_db_directory():
        make_directory("smartHunter", config["default_db_dir"])
    return True

def main() -> bool:
    file_iterator = make_file_iterator()

    parser = Parser(file_iterator=file_iterator)
    parser.main_processing_method()

    return True

if __name__ == "__main__":
    check_and_create_default_dir()
    main()
