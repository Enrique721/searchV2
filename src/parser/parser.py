import re
import datetime
from optparse import Option
from typing import Iterator, Tuple, Optional
from src.db.db_operation import DatabaseOperation

class Parser():

    # <Algo, ?> -> Opcional
    # <Algo, ?, i> -> Opcional e sem distinção de caixa alta ou baixa
    # <Algo, i> -> Sem distinção de caixa alta ou baixa

    # Expressão regular pre compiladas
    re_patterns = [
        # <URL, ?>(" " | ":")<USER | EMAIL>(" " | ":")<PASSWORD>
        # Adicionar suporte para o delimitador , e -
        re.compile(r'(?:(https?:\/\/[^\s:]+)\s*[:\s]+)?([^\s:@]+(?:@[^\s:]+)?)\s*[:\s]+\s*([^\s]\ +)'), 
        #
        # <Link: <URL>, ?, i>
        # <User: <USER | EMAIL>, i>
        # <Password: <PASSWORD>, i>
        # 
        re.compile(r'')
    ]

    def __init__(self,
                 file_iterator: Optional[Iterator[str]],
                 database_operation: DatabaseOperation
             ) -> None:
        self.file_iterator: Iterator[str] = file_iterator
        self.database_operation: DatabaseOperation = database_operation
        self.patterns_type = None

    def main_processing_method(self):
        for file in self.file_iterator:
            self.process_file(file)

    def process_file(self, file: str, chunk_size: int = 800000):

        with open(file, 'r') as f:

            chunk = []
            for line in f:
                credential_instance = self.__extract_line_data(line)
                if credential_instance is dict:
                    chunk.append( credential_instance )

                if len(chunk) >= chunk_size:
                    return

    def __extract_line_data(self, line) -> Optional[dict]:

        for re_compiled_pattern in Parser.re_patterns:

            line_parsed = re_compiled_pattern.search(line)
            if line_parsed:
                url, user, password = line_parsed.groups()

                self.__credential_formatting(
                    url=url,
                    user=user,
                    password=password,
                    register_date= datetime.datetime.now(),
                    access_date=None,
                    leak_date=None,
                    group=None
                )

                credential_instance =  {
                        "url": url,
                        "user": user,
                        "password": password,
                        "data_de_cadastro": datetime.datetime.now(),
                        "valido": True
                    }
                return credential_instance

        return None

    def __credential_formatting(
        self,
        url: str,
        user: str,
        password: str,
        register_date: datetime.datetime,
        access_date: Optional[datetime.datetime],
        leak_date: Optional[datetime.datetime],
        group: Optional[str]
    ) -> dict:

        return {
                    "url": url,
                    "user": user,
                    "password": password,
                    "register_date": datetime.datetime.now(),
                    "group": group,
                    "access_date": None,
                    "leak_date": None,
                }
