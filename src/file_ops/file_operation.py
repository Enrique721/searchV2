import os
import sys
import glob
import pathlib
import itertools
from typing import List, AnyStr, Iterator, Optional
from src.default_config.default_config import config

class DirectoryOperation():

    def __init__(self):
        return

    def check_directory(self, path: str) -> Optional[pathlib.Path]:
        path_object = pathlib.Path(path)

        if path_object.exists():
            return path_object

        return None

    def check_creation_directory(self, path: str) -> pathlib.Path:

        path_status = self.check_directory(path)

        if path_status is None:
            print(f"Erro: Falha ao criar ou encontrar o diretório: {path}", file=sys.stderr)
            sys.exit(1)
        else:
            return path_status

    def create_directory(self, path: str) -> pathlib.Path:

        if not self.check_directory(path):
            os.makedirs(path)
        return self.check_creation_directory(path)


class FileOperation:
    def __init__(self, directory_operation: DirectoryOperation):
        self.directory_operation = directory_operation

    def make_file_iterator(self, extensions: Optional[List[str]] = ["txt", "csv"]) -> Optional[Iterator[str]]:

        if extensions is None:
            return None

        else:
            default_log_dir = config["default_log_consume_dir"]
            log_dir = self.directory_operation.create_directory(default_log_dir)

            path_pattern_list = [f"{str(log_dir)}/*.{extension}" for extension in extensions]
    
            file_iterator = itertools.chain.from_iterable(
                glob.iglob(pattern) for pattern in path_pattern_list
            )

            return file_iterator


if __name__ == "__main__":

    file_operation = FileOperation(DirectoryOperation())
