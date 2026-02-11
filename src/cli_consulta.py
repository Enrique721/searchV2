from src.file_ops.file_operation import DirectoryOperation
from src.db.db_query_builder import QueryBuilder
from src.db.db_operation import DatabaseOperation
from src.db.db_connection import DatabaseConnection
from src.arg_parser.arg_parse import CMDArgumentParser
from src.export.formatter import make_directory, export_data

from typing import Optional, List

import sqlite3
import argparse

def main():
    parser_object = CMDArgumentParser()
    args = parser_object.get_args()

    directory_operation = DirectoryOperation()
    directory = directory_operation.create_directory(
                         args.output if args.output else args.pattern
                     )

    db_connection = DatabaseConnection()

    db_executor = DatabaseOperation(
                        db_connection,
                        query_builder=QueryBuilder()
                    )

    query_result = db_executor.query_executor_search(
        url=args.url,
        username=args.username,
        password=args.password,
        pattern=args.pattern,
        tags=args.tag
    )

    export_data(
        directory=str(directory),
        report_name=args.output if args.output else args.pattern,
        query_result=query_result,
        pattern=args.pattern
    )

    db_connection.closeConnection()

    
if __name__ == "__main__":
    main()
