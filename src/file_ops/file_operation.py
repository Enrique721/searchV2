import itertools
import glob
import sys
import os
import pathlib
from typing import List, AnyStr, Iterator
from src.default_config.default_config import config

def create_default_dir(prepare_dir: str):

    os.makedirs(prepare_dir)

    path_exists = pathlib.Path(prepare_dir)

    if path_exists.exists():
        return path_exists

    print(f"Erro: Arquivo não encontrado: {prepare_dir}", file=sys.stderr)
    sys.exit(1)



def prepare_default_dir(path_string: str):

    path_exists = pathlib.Path(path_string)

    if path_exists.exists():
        return path_exists
    else:
        return create_default_dir(path_string)


def make_file_iterator(extensions: List[str] = ["txt", "csv"]) -> Iterator[str]:

    default_log_dir = config["default_log_consume_dir"]
    log_dir = prepare_default_dir(default_log_dir)

    path_pattern_list = [f"{str(log_dir)}/*.{extension}" for extension in extensions]
    
    print(path_pattern_list)
    
    file_iterator = itertools.chain.from_iterable(
        glob.iglob(pattern) for pattern in path_pattern_list
    )

    return file_iterator

if __name__ == "__main__":
    make_file_iterator()
