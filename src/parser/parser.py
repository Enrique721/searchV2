from src.db.db_operation import DatabaseOperation
import re
import datetime
from optparse import Option
from typing import Iterator, Tuple, Optional

class Parser():

    # <Algo, ?> -> Opcional
    # <Algo, ?, i> -> Opcional e sem distinção de caixa alta ou baixa
    # <Algo, i> -> Sem distinção de caixa alta ou baixa

    # Expressão regular pre compiladas
    re_patterns = [
        # <URL, ?>(" " | ":")<USER | EMAIL>(" " | ":")<PASSWORD>
        # Adicionar suporte para o delimitador , e -
        re.compile(
            r'^(?:(https?:\/\/[^\s:/]+)\s*[:\s]+)?([a-zA-Z0-9._-]+(?:@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})?)\s*[:\s]+\s*([^\s\x00-\x1F\x7F█╔╗╝╚═]+)$'
        ),
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
            self.__process_file(file)

    def __process_file(self, file: str, chunk_size: int = 800000):

        with open(file, 'r') as f:
            chunk = []
            for line in f:
                credential_instance = self.__extract_line_data(line)
                if credential_instance is not None:
                    chunk.append( credential_instance )

                if len(chunk) >= chunk_size:
                    print(chunk)

            if (len(chunk) != 0):
                print("chunk size: ", end="")
                print(len(chunk))

    def __extract_line_data(self, line) -> Optional[dict]:

        for i, re_compiled_pattern in enumerate(Parser.re_patterns):

            line_parsed = re_compiled_pattern.search(line)

            if line_parsed and len(line_parsed.groups()) > 0:
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
                        "date": datetime.datetime.now(),
                        "user": user,
                        "password": password,
                        "group": "askdjl",
                        "compromised_date": datetime.datetime.now(),
                        "arguments": []
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
