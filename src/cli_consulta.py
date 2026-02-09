from src.arg_parser.arg_parse import CMDArgumentParser
from src.db.db_query_builder import QueryBuilder
from src.db.db_operation import DatabaseOperation
from src.db.db_connection import DatabaseConnection
from src.export.formatter import make_directory, export_data

from typing import Optional, List

import sqlite3
import argparse

def main():
    parser_object = CMDArgumentParser()
    args = parser_object.get_args()

    diretorio = make_directory(report_name=args.output if args.output else args.pattern)

    db_connection = DatabaseConnection(args.path)

    db_executor = DatabaseOperation(
                        db_connection,
                        query_builder=QueryBuilder()
                    )

    query_result = db_executor.query_executor(
                        date=args.date,
                        email=args.email,
                        password=args.password,
                        group=args.group,
                        compromised_date=args.compromised_date,
                        include_outdated_credential=args.invalid_credential,
                        pattern=args.pattern
    )

    export_data(
        directory=diretorio,
        report_name=args.output if args.output else args.pattern,
        query_result=query_result
    )

    db_connection.closeConnection()

    
if __name__ == "__main__":
    main()
