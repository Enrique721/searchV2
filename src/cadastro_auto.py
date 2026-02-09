
import os
from pathlib import Path
from typing import Optional

from src.parser.parser import Parser
from src.db.db_operation import DatabaseOperation
from src.db.db_connection import DatabaseConnection
from src.db.db_query_builder import InsertionBuilder
from src.export.formatter import make_directory
from src.default_config.default_config import config
from src.file_ops.file_operation import FileOperation, DirectoryOperation


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
    file_operation = FileOperation(directory_operation=DirectoryOperation())
    database_connection = DatabaseConnection()
    
    database_write_operation = DatabaseOperation(
                                       database_conn=database_connection,
                                       query_builder=InsertionBuilder()
                                   )

    parser = Parser(file_iterator=file_operation.make_file_iterator(),
                        database_operation=database_write_operation
                    )
    parser.main_processing_method()

    return True

if __name__ == "__main__":
    check_and_create_default_dir()
    main()
