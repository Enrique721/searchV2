import os
import sys
import glob
import pathlib
import itertools
from typing import List, AnyStr, Iterator, Optional
from src.default_config.default_config import config

MAX_RETRIES = 100

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

    def __move_file(self, from_path: str, to_path: str):

        path = self.directory_operation.create_directory(to_path)

        if path is None:
            raise OSError("Failed to create directory or path not found")
        
        try:
            os.rename(
                  src=from_path,
                  dst=f"{os.path.join(to_path, os.path.basename(from_path))}")
            return True

        except OSError:
            print("Trying to create a file with suffix")
            base = os.path.basename(from_path)
            name, ext = os.path.splitext(base)
            for i in range(1, MAX_RETRIES + 1):
                new_name = f"{name}_{i}{ext}"
                new_dst = os.path.join(to_path, new_name)

                try:
                    os.rename(from_path, new_dst)
                    return True

                except OSError:
                    print("Failed to created with suffix")
                    pass
        return False

    def move_processed_file(self, target_file: str) -> bool:
        status = self.__move_file(
                     from_path=target_file,
                     to_path=config["default_log_not_processed_dir"]
                 )
        if status:
            print(f"Moved successfully {target_file}")
        else:
            print(f"Failed to move {target_file}")
        
        return status

    def move_unprocessed_file(self, target_file: str) -> bool:
        status = self.__move_file(
                     from_path=target_file,
                     to_path=config["default_log_processed_dir"]
                 )
        if status:
            print(f"Moved successfully {target_file}")
        else:
            print(f"Failed to move {target_file}")

        return status
