import os
import sys
import sqlite3
from pathlib import Path
from typing import Optional, Tuple, List
from src.default_config.default_config import config


# Significado do arguments
# 
# Query
#  -> Padrão a ser procurado
#
# Insertion
#  -> Lista de tags
#
# Update
#  -> A ser definido
#
# Delete
#  -> A ser definido

class QueryBuilder:

    def __init__(self):
        return

    def __build_filter_section(
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
    

    def query_builder(
        self,
        url: bool,
        password: bool,
        username: bool,
        pattern: str,
        tags: Optional[List[str]],
    ) -> Tuple[str, List]:

        query = """
            SELECT
                url, username, password, group_id, compromised_date,
                registration_date, access_date
            FROM credential
            WHERE 1=1
        """

        params = []

        if pattern == "*" or (url == False and password == False and username == False):
            return query, params

        print(url, password, username)
        if url:
            query += f" AND url LIKE ?"
            params.append(f"%{pattern}%")
        if password:
            query += f" AND password LIKE ?"
            params.append(f"%{pattern}%")
        if username:
            query += f" AND username LIKE ?"
            params.append(f"%{pattern}%")

        print(query)
        return query, params

class InsertionBuilder:
    def __init__(self):
        return

    def query_builder(
        self,
        url: Optional[str] = None,
        date: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        group: Optional[str] = None,
        compromised_date: Optional[str] = None,
        arguments: List[str] = [],
    ) -> Tuple[str, List]:
        query_template = InsertionBuilder.query_credential_name_insert_template()

        params = []
        params.append(url)
        params.append(user)
        params.append(password)
        params.append(group)
        params.append(compromised_date)
        params.append(date)

        return query_template, params

    @staticmethod
    def query_credential_name_insert_template():
        return  """
            INSERT INTO credential (
                url, username, password, group_id,
                compromised_date, registration_date, access_date
            ) VALUES (?, ?, ?, ?, ?, ?, NULL)
            ON CONFLICT(username, password, url)
            DO NOTHING
        """

    @staticmethod
    def query_group_name_insert_template():
        return """
            INSERT OR IGNORE INTO group_name (
                name
            ) VALUES ( ? )
        """

    @staticmethod
    def query_tag_insert_template():
        return """
            INSERT OR IGNORE INTO tag (
                name
            ) VALUES ( ? )
        """


# Funcionalidade de update,
# Isso será feito
class UpdateBuilder:
    def __init__(self):
        return

# Funcionalidade de delete
# Se for necessário avisar
class DeleteBuilder:
    def __init__(self):
        return

