from src.db.db_query_builder import QueryBuilder
import os
import sys
import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List
from src.default_config.default_config import config

class DatabaseConnection:

    def __init__(self, path: Optional[str] = None) -> None:
        path_to_db = DatabaseConnection.__check_db_file_existence(path if path else None)
        self.connection_object = DatabaseConnection.__create_sqlite3_connection(path_to_db)

    @staticmethod
    def __check_db_file_existence(path: Optional[str]) -> str:
        default_db_file = os.path.join(
                 config["default_db_dir"],
                 config["default_db_file"]
             )
        path_exists = Path(path if path else default_db_file)

        if (path_exists.exists()):
            return str(path_exists)
        else:
            print(f"Erro: Arquivo não encontrado: {path}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def __create_sqlite3_connection(path: str) -> sqlite3.Connection:
        return sqlite3.connect(path)

    def getConnectionObject(self) -> sqlite3.Connection:
        return self.connection_object

    def closeConnection(self) -> None:
        self.connection_object.close()
