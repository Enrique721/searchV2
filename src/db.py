import os
import sys
from pathlib import Path
from typing import Optional, Tuple, List
import sqlite3

def check_file(path: str) -> str:
    pathExists = Path(path)
    if (pathExists.exists()):
        return path
    else:
        print(f"Erro: Arquivo não encontrado: {path}", file=sys.stderr)
        sys.exit(1)

def create_sqlite3_connection(
    path: Optional[str] = None
) -> sqlite3.Connection :

    # Default
    if path is None or len(path) == 0:
        default_path = check_file(f"{os.environ.get('HOME')}/.local/share/smartHunter/smartHunter.db")
        return sqlite3.connect(default_path)

    # Check file
    path = check_file(path)
    return sqlite3.connect(path)

def buildFilterSection(
        field_name: str,
        field: Optional[str],
        pattern: str,
        params: List,
        operator: str
    ) -> Optional[str]:

    if field or operator == "LIKE":
        params.append(field if field else pattern)
        return f" AND {field_name} {operator} ?"

def queryBuilder(
    date: Optional[str],
    email: Optional[str],
    password: Optional[str],
    group: Optional[str],
    compromised_date: Optional[str],
    include_outdated_credential: bool,
    pattern: str
) -> Tuple[str, List]:

    query = """
        SELECT
            email,
            password,
            date,
            valid,
            compromised_date,
            group
        FROM credentials
        WHERE 1=1
    """

    params = []

    buildFilterSection(
        field_name="group",
        field=group,
        pattern=pattern,
        params=params,
        operator="="
    )

    buildFilterSection(
        field_name="compromised_date",
        field=compromised_date,
        pattern=pattern,
        params=params,
        operator="="
    )

    buildFilterSection(
        field_name="date",
        field=date,
        pattern=pattern,
        params=params,
        operator="="
    )

    buildFilterSection(
        field_name="email",
        field=email,
        pattern=pattern,
        params=params,
        operator="LIKE"
    )

    buildFilterSection(
        field_name="password",
        field=password,
        pattern=pattern,
        params=params,
        operator="LIKE"
    )

    if not include_outdated_credential:
        query += " AND valid = 1"

    return query, params

def queryExecute(
    queryString: str,
    conn: sqlite3.Connection,
    params: List
) -> List[Tuple]:
    cursor = conn.cursor()
    cursor.execute(queryString, params)
    return cursor.fetchall()

def close_sqlite3_connection(conn: sqlite3.Connection) -> None:
    conn.close()

def queryExecutor(
    conn: sqlite3.Connection,
    date: Optional[str],
    email: Optional[str],
    password: Optional[str],
    group: Optional[str],
    compromised_date: Optional[str],
    include_outdated_credential: bool,
    pattern: str,
):
    query_string, params = queryBuilder(
                                date=date,
                                email=email,
                                password=password,
                                group=group,
                                compromised_date=compromised_date,
                                include_outdated_credential=include_outdated_credential,
                                pattern=pattern
                            )

    queryResult = queryExecute(
                           query_string,
                           conn,
                           params
                       )
    return queryResult
