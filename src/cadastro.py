
import os
from pathlib import Path
from typing import Optional

from src.db.db_operation import DatabaseOperation
from src.db.db_connection import DatabaseConnection
from src.db.db_query_builder import InsertionBuilder
from src.parser.parser import Parser
from src.export.formatter import make_directory
from src.default_config.default_config import config
from src.file_ops.file_operation import FileOperation, DirectoryOperation

def main():
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

    database_connection.closeConnection()

if __name__ == "__main__":
    main()
