import os
from src.constant.constant import MAX_CHUNK_SIZE
from src.parser.block_data_parser import ParseBlockData
from src.data_normalization.url_normalization import UrlNormalization
from src.db.db_operation import DatabaseOperation

import re
import datetime
from typing import Iterator, Tuple, Optional

from enum import Enum

class ParserType(Enum):
    LINE_PARSING = 0
    BLOCK_PARSING = 1
    OK_MATCH_PARSING = 2

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

        # <protocolo + URL, ?>(" " | ":" | "|")<USER | EMAIL>(" " | ":" | "|")<PASSWORD>
        # Adicionar suporte para o delimitador , e - <- Fase de refinamento
        re.compile(
            r"""(?ix)
            ^(?!\s*(?:link|url|site|user|login|email|username|password|pass)\s*:)
            (?:
                (
                    (?:[a-zA-Z][a-zA-Z0-9+.-]*:\/\/.+?|www\.\S+?)
                    (?::\d+)?
                )
                \s*[:| ]\s*
            )?
            ([^\s:|█╔╗╚╝═║]+)
            \s*[:| ]\s*
            ([^\s:|█╔╗╚╝═║]+)
            \s*$
            """,
            re.IGNORECASE
        ),
        
        # <Link: <URL>, ?, i>
        # <User: <USER | EMAIL>, i>
        # <Password: <PASSWORD>, i>
        # Se achar a tag e completar um ciclo capturar o bloco e colocar no array de cred
        {
            BlockSegment.LINK: re.compile(r"(?i)^(link|url|site)\s*:\s*(.+)$"),
            BlockSegment.USER: re.compile(r"(?i)^(user|login|email|username)\s*:\s*(.+)$"),
            BlockSegment.PASSWORD: re.compile(r"(?i)^(password|pass)\s*:\s*(.+)$"),
        },

        # Username:password |(*)?+
        re.compile(r'^([^:]+):\s*([^|]+?)\s*(?=\|)', re.IGNORECASE)
    ]

    def __init__(self,
                 file_iterator: Optional[Iterator[str]],
                 database_operation: DatabaseOperation
             ) -> None:
        self.file_iterator: Iterator[str] = file_iterator
        self.database_operation: DatabaseOperation = database_operation

        #
        # LOGIN: <str>
        # PASSWORD: <str>
        # 
        self.block_instance: dict[str, Optional[str]] = ParseBlockData.generate_new_block()

        # Today time stamp
        self.today_time = datetime.datetime.now().isoformat()

        # Chunk para inserir dados em massa limitado 80
        self.chunk = []

    def main_processing_method(self):
        for file in self.file_iterator:
            print("----------------------------------------")
            print("Processing: ", file)

            self.__process_file(file)

            print("Processing Finished Processing: ", file)
            print("----------------------------------------")

    def __process_file(self, file: str, chunk_size: int = MAX_CHUNK_SIZE):
        group_name, collection_date = self.__get_group_name(file)

        with open(file, 'r') as f:
            self.read_process_file(
                file=f,
                chunk_size=chunk_size,
                group_name=group_name,
                collection_date=collection_date
            )

            if len(self.block_instance.keys()) != 0:
                self.__add_block_data_to_chunk()
            
            if len(self.chunk) != 0:
                self.database_operation.\
                    bulk_operation_insert_execute(
                        data=self.chunk,
                        group_name=group_name,
                        collection_date=collection_date
                    )

        self.chunk = []

    def read_process_file(self,
                          file,
                          chunk_size,
                          group_name,
                          collection_date):

       for line in file:
            credential_instance = self.__extract_data(line=line.strip(' /\t\n'))
            if credential_instance is not None:
                self.chunk.append( credential_instance )

            if len(self.chunk) >= chunk_size:
                self.database_operation.\
                    bulk_operation_insert_execute(
                        data=self.chunk,
                        group_name=group_name,
                        collection_date=collection_date
                    )
                self.chunk = []

    # Identificação do modo a ser utilizado para o parsing
    def __extract_data(self, line) -> Optional[dict]:
        for i, re_compiled_pattern in enumerate(Parser.re_patterns):

            res = None
            if ParserType.LINE_PARSING.value == i:
                res = self.__extract_line_data(re_compiled_pattern, line)

            elif ParserType.BLOCK_PARSING.value == i:
                res = self.__extract_block_data(re_compiled_pattern, line)

            elif ParserType.OK_MATCH_PARSING.value == i:
                res = self.__extract_line_data(re_compiled_pattern, line)

            if res is not None:
                return res

        return None

    def __extract_line_data(self,
                            re_pattern_matcher: re.Pattern,
                            line: str):

        line_parsed = re_pattern_matcher.search(line)
        
        if line_parsed and len(line_parsed.groups()) > 0:

            if (len(line_parsed.groups()) == 2):
                url, user, password = ("", *line_parsed.groups())
            else:
                url, user, password = line_parsed.groups()

            if password is not None and password.startswith('//'):
                if not re_pattern_matcher.match(password.lstrip('/ ')):
                    return None
 
            url_parsed, status = UrlNormalization.normalization(url) if url else ('', False)

            credential_instance = self.__credential_formatting(
                url=url_parsed,
                user=user,
                password=password,
                leak_date=None,
                group=None
            )

            return credential_instance
        
        return None

    def __extract_block_data(self, re_pattern_matcher: dict[BlockSegment, re.Pattern], line: str):

        for segment, pattern in re_pattern_matcher.items():
            matched = pattern.search(line)
            if not matched:
                continue

            if self.block_instance.get(segment.column) is not None:
                self.__add_block_data_to_chunk()

            data = matched.group(2).strip()
            self.block_instance[segment.column] = data
        return None

    def __add_block_data_to_chunk(self):
        self.chunk.append(self.__credential_formatting(
            url=self.block_instance.get("url") if self.block_instance.get("url") else "",
            user=self.block_instance.get("user") if self.block_instance.get("user") else "",
            password=self.block_instance.get("password") if self.block_instance.get("password") else "",
            leak_date=None,
            group=None,
        ))
        self.block_instance = ParseBlockData.generate_new_block()
        
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
                    "registration_date": self.today_time,
                    "compromised_date": leak_date,
                    "group": group,
                    "access_date": None,
                }

    # Por favor colocar a data em formato padrão do ISO
    # Valor de retorno group name e collection date
    def __get_group_name(self, file: str)-> Tuple[str, str]:

        base_file_name = os.path.basename(file)

        splitted_values = base_file_name.split('.')

        if len(splitted_values) == 1:
            return splitted_values[0], datetime.datetime.now().date()


        # Remove extensão
        filename, _ = (splitted_values[0], splitted_values[-1])

        # Defaulting
        if '_' not in filename:
            return filename, datetime.datetime.now().date()

        # Categoria_Nome-Grupo_data_hash
        # Vamos extrair o Nome-Grupo e a data
        # [Categoria, Nome-Grupo, Data, Hash]
        file_name_section_split = filename.split('_')

        if len(file_name_section_split) < 4:
            return "Unknown", datetime.datetime.now().date() 

        group_name, collection_date = (file_name_section_split[1],
                                       file_name_section_split[2])

        return group_name, collection_date