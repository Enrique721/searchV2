from src.data_normalization.url_normalization import UrlNormalization
from src.db.db_operation import DatabaseOperation
import re
import datetime
from optparse import Option
from typing import Iterator, Tuple, Optional, List

from enum import Enum

class ParserType(Enum):
    LINE_PARSING = 0
    BLOCK_PARSING = 1

class BlockSegment(Enum):
    LINK = 0
    USER = 1
    PASSWORD = 2

    @property
    def column(self) -> str:
        return {
            BlockSegment.LINK: "url",
            BlockSegment.USER: "user",
            BlockSegment.PASSWORD: "password",
        }[self]

class Parser:

    # <Algo, ?> -> Opcional
    # <Algo, ?, i> -> Opcional e sem distinção de caixa alta ou baixa
    # <Algo, i> -> Sem distinção de caixa alta ou baixa

    # Expressão regular pre compiladas
    re_patterns = [

        # <protocolo + URL, ?>(" " | ":")<USER | EMAIL>(" " | ":")<PASSWORD>
        # Adicionar suporte para o delimitador , e - <- Fase de refinamento
        re.compile(
            r'^(?:([a-zA-Z][a-zA-Z0-9+.-]*:\/\/[^\s]+)\s*[:\s]+)?'
            r'((?:\+?\d{1,3})?\d{8,15}|[a-zA-Z0-9._-]+(?:@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})?)'
            r'\s*[:\s]+\s*'
            r'([^\s\x00-\x1F\x7F█╔╗╝╚═]+)$'
        ),


        # <Link: <URL>, ?, i>
        # <User: <USER | EMAIL>, i>
        # <Password: <PASSWORD>, i>
        {
            BlockSegment.LINK: re.compile(r"(?i)^(link|url|site)\s*:\s*(.+)$"),
            BlockSegment.USER: re.compile(r"(?i)^(user|login|email)\s*:\s*(.+)$"),
            BlockSegment.PASSWORD: re.compile(r"(?i)^(password|pass)\s*:\s*(.+)$"),
        }

    ]

    ## Check the proportion of ascii chars
    def sane(s: str) -> bool:
        return sum(c.isascii() for c in s) / len(s) > 0.9

    def __init__(self,
                 file_iterator: Optional[Iterator[str]],
                 database_operation: DatabaseOperation
             ) -> None:
        self.file_iterator: Iterator[str] = file_iterator
        self.database_operation: DatabaseOperation = database_operation
        self.block_instance: dict[str, Optional[str]] = {}
        self.chunk = []

    def main_processing_method(self):
        for file in self.file_iterator:
            self.__process_file(file)

    def __process_file(self, file: str, chunk_size: int = 800000):

        with open(file, 'r') as f:

            for line in f:
                credential_instance = self.__extract_data(line=line.strip(' /\t'))
                if credential_instance is not None:
                    self.chunk.append( credential_instance )

                if len(self.chunk) >= chunk_size:
                    self.database_operation.\
                        bulk_operation_insert_execute(data=self.chunk)
                    self.chunk = []

            if len(self.block_instance.keys()) != 0:
                self.__add_block_data_to_chunk()
            
            if (len(self.chunk) != 0):
                self.database_operation.\
                    bulk_operation_insert_execute(data=self.chunk)

        self.chunk = []

    # Modo de parsing
    # Com força bruta
    def __extract_data(self, line) -> Optional[dict]:
        for i, re_compiled_pattern in enumerate(Parser.re_patterns):

            res = None
            if ParserType.LINE_PARSING.value == i:
                res = self.__extract_line_data(re_compiled_pattern, line)

            elif ParserType.BLOCK_PARSING.value == i:
                res = self.__extract_block_data(re_compiled_pattern, line)

            if res is not None:
                return res

        return None

    def __extract_line_data(self, re_pattern_matcher: re.Pattern, line: str):

        line_parsed = re_pattern_matcher.search(line)
        
        if line_parsed and len(line_parsed.groups()) > 0:
            url, user, password = line_parsed.groups()
            url = UrlNormalization.normalization(url) if url else ''

            credential_instance = self.__credential_formatting(
                url=url, user=user, password=password,
                leak_date=None, group=None
            )

            return credential_instance
        
        return None

    def __extract_block_data(self, re_pattern_matcher: dict[BlockSegment, re.Pattern], line: str):

        for segment, pattern in re_pattern_matcher.items():
            matched = pattern.search(line)
            if matched and matched.group(1):
                if self.block_instance.get(segment.column) is not None:
                    self.__add_block_data_to_chunk()
                    
                self.block_instance[segment.column] = matched.group(1).strip()
        return None

    def __add_block_data_to_chunk(self):
        self.chunk.append(self.__credential_formatting(
            url=self.block_instance.get("url"),
            user=self.block_instance.get("user"),
            password=self.block_instance.get("password"),
            leak_date=None,
            group=None,
        ))
        self.block_instance = {}
        
    def __credential_formatting(
        self,
        url: Optional[str],
        user: Optional[str],
        password: Optional[str],
        leak_date: Optional[datetime.datetime],
        group: Optional[str]
    ) -> dict:

        return {
                    "url": url,
                    "user": user,
                    "password": password,
                    "registration_date": datetime.\
                                            datetime.\
                                            now().\
                                            isoformat(),
                    "group": group,
                    "compromised_date": leak_date,
                    "access_date": None,
                }
