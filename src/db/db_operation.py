from src.db.db import DatabaseConnection
from src.db.db_query_builder import QueryBuilder
import os
import sys
import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List
from src.default_config.default_config import config

class DatabaseOperation:

    def __init__(
                 self,
                 database_conn: DatabaseConnection,
                 query_builder: QueryBuilder
             ):
        self.database_connection_object = database_conn
        self.database_query_builder = query_builder

    def __buildFilterSection(
            self,
            field_name: str,
            field: Optional[str],
            pattern: str,
            params: List,
            operator: str,
            fallback_operator: Optional[str] = None
        ) -> Optional[str]:

        if field or operator == "LIKE":
            params.append(field if field else pattern)
            return f" AND {field_name} {operator} ?"

        if fallback_operator is not None:
            return f" AND {field_name} {fallback_operator}"
    
    def query_execute(
        self,
        queryString: str,
        conn: sqlite3.Connection,
        params: List
    ) -> List[Tuple]:
        cursor = conn.cursor()
        cursor.execute(queryString, params)
        return cursor.fetchall()


    def query_executor(
        self,
        conn: sqlite3.Connection,
        date: Optional[str],
        email: Optional[str],
        password: Optional[str],
        group: Optional[str],
        compromised_date: Optional[str],
        include_outdated_credential: bool,
        pattern: str,
    ):
        query_string, params = self.database_query_builder.query_builder(
                                    date=date,
                                    email=email,
                                    password=password,
                                    group=group,
                                    compromised_date=compromised_date,
                                    include_outdated_credential=include_outdated_credential,
                                    pattern=pattern
                                )

        query_result = self.query_execute(
                               query_string,
                               conn,
                               params
                           )

        return query_result


