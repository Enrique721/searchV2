from src.db.db_connection import DatabaseConnection
from src.db.db_query_builder import QueryBuilder, InsertionBuilder

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
                 query_builder
             ):
        self.database_connection_object = database_conn
        self.database_query_builder = query_builder
    
    # Usado somente no select por enquanto
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
        password: bool,
        username: bool,
        tags: Optional[List[str]],
        pattern: str
    ):

        query_statement, params = self.database_query_builder.query_builder(
            url=url,
            password=password,
            username=username,
            pattern=pattern,
            tags=tags
        )

        query_result = self.__query_execute(
            query_statement,
            params
        )
        
        return query_result

    def query_executor(
        self,
        url: Optional[str],
        date: Optional[str],
        user: Optional[str],
        password: Optional[str],
        group: Optional[str],
        compromised_date: Optional[str],
        include_outdated_credential: bool,
        pattern: str,
    ):
        query_string, params = self.database_query_builder.query_builder(
                                    url=url,
                                    date=date,
                                    user=user,
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
    
    def bulk_operation_insert_execute(self, data: List[BulkOperationItem]):

        param_list = []
        query_statement = ""

        if data[0].get("group") is not None:
            group = data[0].get("group")
            group_name_insert_template = InsertionBuilder.query_group_name_insert_template()
            tag_insertion_query = InsertionBuilder.query_tag_insert_template()
            connection_object  = self.database_connection_object.getConnectionObject()
            cursor = connection_object.cursor()
            self.__query_execute_insert(group_name_insert_template, [group])
            self.__query_execute_insert(tag_insertion_query, [group])


       
        query_string, params = self.database_query_builder.query_builder(
            url=data[0].get("url"),
            date= data[0].get("date"),
            user= data[0].get("user"),
            password= data[0].get("password"),
            group=data[0].get("group"),
            compromised_date=data[0].get("compromised_date"),
            arguments=[]
        )

        for dataItemIdx in range(1, len(data)):

            dataItem = data[dataItemIdx]
            query_string, params = self.database_query_builder.query_builder(
                url=dataItem.get("url"),
                date=dataItem.get("registration_date"),
                user=dataItem.get("user"),
                password=dataItem.get("password"),
                group=dataItem.get("group"),
                compromised_date=dataItem.get("compromised_date"),
                arguments=[]
            )

            param_list.append(params)
        
        query_result = self.__execute_query_many(
            query_string,
            param_list
        )


    def __execute_query_many(self, query_string: str, params: List[List[str]]):


        conn = self.database_connection_object.getConnectionObject()
        
        conn.execute("BEGIN")

        cursor = conn.cursor()

        res = cursor.executemany(query_string, params)

        conn.commit()

        print(cursor.rowcount)
        return res
