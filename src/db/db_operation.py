from src.db.db_connection import DatabaseConnection
from src.db.db_query_builder import QueryBuilder, DatabaseActionInterface
import os
import sys
import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List, TypedDict
from src.default_config.default_config import config

class BulkOperationItem(TypedDict):
    date: Optional[str]
    email: Optional[str]
    password: Optional[str]
    group: Optional[str]
    compromised_date: Optional[str]
    include_outdated_credential: bool
    pattern: str


class DatabaseOperation:

    def __init__(
                 self,
                 database_conn: DatabaseConnection,
                 query_builder: DatabaseActionInterface
             ):
        self.database_connection_object = database_conn
        self.database_query_builder = query_builder
    
    def __query_execute(
        self,
        queryString: str,
        params: List
    ) -> List[Tuple]:

        cursor = self.\
                    database_connection_object.\
                    getConnectionObject().\
                    cursor()

        cursor.execute(queryString, params)
        return cursor.fetchall()


    def query_executor(
        self,
        url: Optional[str],
        date: Optional[str],
        email: Optional[str],
        password: Optional[str],
        group: Optional[str],
        compromised_date: Optional[str],
        include_outdated_credential: bool,
        pattern: str,
    ):
        query_string, params = self.database_query_builder.query_builder(
                                    url=url,
                                    date=date,
                                    email=email,
                                    password=password,
                                    group=group,
                                    compromised_date=compromised_date,
                                    arguments=[pattern]
                                )

        query_result = self.__query_execute(
                               query_string,
                               params
                           )

        return query_result

    def bulk_operation_execute( self, data: List[BulkOperationItem] ):

        for dataItem in data:
            query_string, params = self.database_query_builder.query_builder(
                url=dataItem.get("url"),
                date= dataItem.get("date"),
                email= dataItem.get("email"),
                password= dataItem.get("pwd"),
                group=dataItem.get("group"),
                compromised_date=dataItem.get("compromised_date"),
                arguments=[]
            )
        return


    def sql_cmd_execute(self, cmd):
        return
