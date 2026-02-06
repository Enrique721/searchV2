import datetime
import re
from typing import Iterator

class Parser():

    generic_re_pattern = re.compile(r'(?:(https?:\/\/[^\s:]+)\s*[:\s]+)?([^\s:@]+(?:@[^\s:]+)?)\s*[:\s]+\s*([^\s]\ +)')

    def __init__(self, file_iterator) -> None:
        self.file_iterator: Iterator[str] = file_iterator
        self.patterns_type = None

    def main_processing_method(self):
        for file in self.file_iterator:
            self.process_file(file)

    def process_file(self, file: str, chunk_size: int = 800000):

        with open(file, 'r') as f:

            chunk = []
            for line in f:
                line_parsed = Parser.generic_re_pattern.search(line)
                if line_parsed:
                    url, user, password = line_parsed.groups()
                    credential_instance =  {
                            "url": url,
                            "user": user,
                            "password": password,
                            "data_de_cadastro": datetime.datetime.now(),
                            "valido": True
                        }
                    chunk.append( credential_instance )

                    if chunk_size >= chunk_size:
                        return





    def extract_line_data(self, line):

        line_parsed = Parser.generic_re_pattern.search(line)

        if line_parsed:
            url,  email, password = line_parsed.groups()
