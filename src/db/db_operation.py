from src.db.db_connection import DatabaseConnection
from src.db.db_query_builder import QueryBuilder, InsertionBuilder
from src.default_config.default_config import config

import os
import sys
import sqlite3

from pathlib import Path
from typing import Optional, Tuple, List, TypedDict

class BulkCredentialInsertOperationItem(TypedDict):
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
                 query_builder
             ):
        self.database_connection_object = database_conn
        self.database_query_builder = query_builder
    
    # Usado somente no select por enquanto
    def __query_execute_fetch(
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

    def __query_execute_insert(
        self,
        queryString: str,
        params: List
    ):

        conn = self.database_connection_object.getConnectionObject()
        cursor = conn.cursor()

        cursor.execute(queryString, params)
        conn.commit()
        return cursor.lastrowid

    def query_executor_search(
        self,
        url: bool,
        username: bool,
        tags: Optional[List[str]],
        pattern: str,
        password: bool = False,
    ):
        query_statement = QueryBuilder.search_query_template()

        params = self.database_query_builder.query_builder(
            url=url,
            password=password,
            username=username,
            pattern=pattern,
            tags=tags
        )

        query_result = self.__query_execute_fetch(
            query_statement,
            params
        )
        
        return query_result

    def bulk_operation_insert_execute(self, data: List[BulkCredentialInsertOperationItem]):

        param_list = []
        group_id = None
        group_name = data[0].get("group")

        if group_name is not None:
            self.__group_name_insertion(group_name)
        
        credential_insertion_query_string = InsertionBuilder \
                                                .query_credential_name_insert_template()

        # Prepare query parameters
        for dataItemIdx in range(0, len(data)):
            dataItem = data[dataItemIdx]
            params = self.database_query_builder.query_builder(
                url=dataItem.get("url"),
                date=dataItem.get("registration_date"),
                user=dataItem.get("user"),
                password=dataItem.get("password"),
                group=dataItem.get("group"),
                compromised_date=dataItem.get("compromised_date"),
                arguments=[]
            )

            param_list.append(params)

        query_result = self.__execute_bulk_operation(
            credential_insertion_query_string,
            param_list
        )

    def __group_name_insertion(self, group_name: str):
        group = group_name
        tag_insert_template = InsertionBuilder.query_tag_insert_template()
        group_name_insert_template = InsertionBuilder.query_group_name_insert_template()

        connection_object = self.database_connection_object.getConnectionObject()
        cursor = connection_object.cursor()

        group_id = self.__query_execute_insert(
                               group_name_insert_template,
                               [group]
                           )

        self.__query_execute_insert(tag_insert_template, [group])

    def __execute_bulk_operation(self, query_string: str, param_list: List[List[str]]):
        conn = self.database_connection_object\
                        .getConnectionObject()
        
        conn.execute("BEGIN")
        cursor = conn.cursor()
        res = cursor.executemany(query_string, param_list)
        conn.commit()

        print("Inseridos: ", cursor.rowcount)
        return res
