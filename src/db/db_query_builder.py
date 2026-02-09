from xml.etree.ElementInclude import include
from pyexpat.errors import XML_ERROR_TEXT_DECL
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

class DatabaseActionInterface:

    def query_builder(
        self,
        url: Optional[str],
        date: Optional[str],
        user: Optional[str],
        password: Optional[str],
        group: Optional[str],
        compromised_date: Optional[str],
        arguments: List[str],
    ):
        pass

class QueryBuilder(DatabaseActionInterface):

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
        url: Optional[str],
        date: Optional[str],
        user: Optional[str],
        password: Optional[str],
        group: Optional[str],
        compromised_date: Optional[str],
        arguments: List[str],
    ) -> Tuple[str, List]:

        if arguments is None or len(arguments) == 0:
            raise TypeError("Argumento inválido fornecido em busca")

        pattern = arguments[0]

        query = """
            SELECT
                url, email, password, group, compromised_date,
                registration_date, access_date
            FROM credentials
            WHERE 1=1
        """

        params = []

        if pattern == "*":
            return query, params

        self.__build_filter_section(
            field_name="group",
            field=group,
            pattern=pattern,
            params=params,
            operator="=",
            fallback_operator="LIKE"
        )

        self.__build_filter_section(
            field_name="compromised_date",
            field=compromised_date,
            pattern=pattern,
            params=params,
            operator="=",
        )

        self.__build_filter_section(
            field_name="date",
            field=date,
            pattern=pattern,
            params=params,
            operator="=",
            fallback_operator="LIKE"
        )

        self.__build_filter_section(
            field_name="user",
            field=user,
            pattern=pattern,
            params=params,
            operator="LIKE",
        )

        self.__build_filter_section(
            field_name="password",
            field=password,
            pattern=pattern,
            params=params,
            operator="LIKE"
        )

        return query, params

class InsertionBuilder(DatabaseActionInterface):
    def __init__(self):
        return

    def query_builder(
        self,
        url: Optional[str],
        date: Optional[str],
        user: Optional[str],
        password: Optional[str],
        group: Optional[str],
        compromised_date: Optional[str],
        arguments: List[str],
    ) -> Tuple[str, List]:
        query_template = InsertionBuilder.query_template()

        params = []
        params.append(url)
        params.append(user)
        params.append(password)
        params.append(group)
        params.append(compromised_date)
        params.append(date)


        return query_template, params


    @staticmethod
    def query_template():
        return  """INSERT INTO crendential (
                url, email, password, group, compromised_date,
                registration_date, access_date
            ) VALUES ( ?, ?, ?, ?, ?, ?, NULL)"""        



class UpdateBuilder:
    def __init__(self):
        return

# Funcionalidade de delete não é prioridade
# Se for necessário avisar
class DeleteBuilder:
    def __init__(self):
        return

