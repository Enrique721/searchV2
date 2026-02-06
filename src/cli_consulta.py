from src.export.formatter import make_directory, export_data
from src.db.db import create_sqlite3_connection, queryExecutor, close_sqlite3_connection

from src.arg_parser.arg_parse import argument_parse
from typing import Optional, List

import sqlite3
import argparse

def main():
    parsed = argument_parse()

    args = parsed.parse_args()

    diretorio = make_directory(report_name=args.output if args.output else args.pattern)

    db_connection = create_sqlite3_connection(args.path)

    query_result = queryExecutor(
                     conn=db_connection,
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

    close_sqlite3_connection(db_connection)

    
if __name__ == "__main__":
    main()
