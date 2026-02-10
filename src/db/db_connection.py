from src.file_ops.file_operation import DirectoryOperation
from src.db.db_query_builder import QueryBuilder
import os
import sys
import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List
from src.default_config.default_config import config

class DatabaseConnection:

    def __init__(self,
                 path: Optional[str] = None) -> None:
        path_to_db = self.__check_db_file_existence(path if path else None)
        self.connection_object = DatabaseConnection.__create_sqlite3_connection(path_to_db)

    def __check_db_file_existence(self, path: Optional[str]) -> str:
        default_db_file = os.path.join( config["default_db_dir"], config["default_db_file"] )
        path_file_exists = Path(path if path else default_db_file)

        directory_operation = DirectoryOperation()
        directory_operation.create_directory(config["default_db_dir"])


        return str(path_file_exists)

    # Depois colocar um try except para tratamento de erro
    @staticmethod
    def __create_sqlite3_connection(path: str) -> sqlite3.Connection:
        if Path(path).exists():
            print("Banco de dados detectado, utilizando o banco de dados existente...")
            return sqlite3.connect(path)
        else:
            print("Banco de dados não detectado, criando um novo e configurando...")
            conn=sqlite3.connect(path)
            DatabaseConnection.__configure_database(connection=conn)
            return conn
    

    def getConnectionObject(self) -> sqlite3.Connection:
        return self.connection_object

    def closeConnection(self) -> None:
        self.connection_object.close()

    @staticmethod
    def __configure_database(connection: sqlite3.Connection): 
        cursor = connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credential (
                cred_id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                username TEXT,
                password TEXT,
                registration_date TEXT,
                access_date TEXT,
                compromised_date TEXT,

                group_id INTEGER,
                FOREIGN KEY (group_id) REFERENCES group_name(group_id),
                UNIQUE (username, password, url)
            )
        """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS tagged_credential (
                               cred_id INTEGER NOT NULL,
                               tag_id INTEGER NOT NULL,

                               PRIMARY KEY (cred_id, tag_id),

                               FOREIGN KEY (cred_id) REFERENCES credential(cred_id),
                               FOREIGN KEY (tag_id) REFERENCES tag(tag_id)
                           )
                       """)


        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS group_name(
                           group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           UNIQUE(name)
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS tag(
                           tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           UNIQUE(name)
                       )
                       """)

        cursor.execute("""CREATE INDEX IF NOT EXISTS idx_credential_username
                               ON credential(username)""")

        cursor.execute("""CREATE INDEX IF NOT EXISTS idx_credential_group
                               ON credential(group_id)""")

        cursor.execute("""CREATE INDEX IF NOT EXISTS idx_tagged_cred_id
                               ON tagged_credential(cred_id)""")

        cursor.execute("""CREATE INDEX IF NOT EXISTS idx_tagged_tag_id
                               ON tagged_credential(tag_id)""")
