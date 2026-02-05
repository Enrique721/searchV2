
from src.arg_parser.arg_parse import argument_parse
from src.formatter import export_data, make_directory
from typing import Optional, List
from src.db import create_sqlite3_connection, queryBuilder, queryExecute, queryExecutor

import sqlite3
import argparse

def main():
    parsed = argument_parse()

    diretorio = make_directory(report_name=parsed.output if parsed.output else parsed.pattern)

    db_connection = create_sqlite3_connection(parsed.path)

    query_result = queryExecutor(
                     conn=db_connection,
                     date=parsed.date,
                     email=parsed.email,
                     password=parsed.password,
                     group=parsed.group,
                     compromised_date=parsed.compromised_date,
                     include_outdated_credential=parsed.invalid_credential,
                     pattern=parsed.pattern
                 )

    export_data(
        directory=diretorio,
        report_name=parsed.output if parsed.output else parsed.pattern,
        query_result=query_result
    )


if __name__ == "__main__":
    main()
