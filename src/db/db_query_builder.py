from typing import Optional,List
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

    @staticmethod
    def search_group_id_template():
        return """
            SELECT group_id
                FROM group_name
                WHERE name = ?
        """

    @staticmethod
    def search_query_template():
        return  """
            SELECT c.url, c.username, c.password, c.registration_date
                FROM credential c
                JOIN credential_text_index f
                    ON c.cred_id = f.rowid
                WHERE credential_text_index MATCH ?;
        """

    def query_builder(
        self,
        url: bool,
        password: bool,
        username: bool,
        pattern: str,
        tags: Optional[List[str]],
    ) -> List:

        params = []

        if pattern is None or len(pattern.strip()) == 0:
            return None

        if '.' in pattern or ':' in pattern or '/' in pattern:
            pattern = f'"{pattern}"'

        # Ambos falsos ou verdadeiros
        if url == username:
            params.append(pattern)

        elif url:
            params.append(f"url:{pattern}")

        elif username:
            params.append(f"username:{pattern}")

        return params


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
    ) -> List:

        params = []
        params.append(url)
        params.append(user)
        params.append(password)
        params.append(group)
        params.append(compromised_date)
        params.append(date)

        return params

    @staticmethod
    def query_credential_name_insert_template():
        return  """
            INSERT INTO credential (
                url,
                username,
                password,
                group_id,
                compromised_date,
                registration_date,
                access_date
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                NULL)
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

