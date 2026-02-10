from src.export.banner import banner
from pathlib import Path
import sqlite3
from datetime import datetime
import time
import sys
import os
from typing import List, Optional, Tuple, Iterable

def make_directory(report_name: str, path_dir: Optional[str]= None) -> str:
    directory = os.path.join(
                 os.getcwd() if not path_dir or len(path_dir) == 0 else path_dir,
                 report_name.replace(" ", "_")
             )
    try:
        os.makedirs(directory)
        return directory
    except OSError:
        print(
              f"Erro: Diretório {directory} já existe",
              file=sys.stderr
          )
        sys.exit(1)
    
## Suporte para row somente no momento
# csv, row, json
def export_data(
    directory: str,
    report_name: str,
    query_result: List,
    pattern: str,
    export_type: str = "row",
):

    if export_type == "row":
        _export_row(directory=directory,
                    report_name=report_name + ".txt",
                    rows=query_result,
                    pattern=pattern)

def _export_row(
    directory: str,
    report_name: str,
    rows: List[Tuple],
    pattern: str,
):
    output_path = Path(directory) / report_name
    user_name_path = Path(directory) / "user.txt"
    password_path = Path(directory) / "password.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=" * 131 + "\n")
        f.write(f"{banner}\n")
        f.write("=" * 131 + "\n")
        f.write("Relatório de busca SmartHunter\n")
        f.write("=" * 131 + "\n")
        f.write(f"Gerado as : {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
        f.write(f"Registros encontrados: {len(rows)}\n")
        f.write(f"Termo de pesquisa: {pattern}\n")
        f.write("=" * 131 + "\n")


        if len(rows) == 0:
            f.write("-" * 60 + "\n")
            f.write("Nada foi encontrado :|\n")
            f.write("-" * 60 + "\n")
            return

        with open(user_name_path, "w", encoding="utf-8") as u:
            with open(password_path, "w", encoding="utf-8") as p:
                for row  in rows:
                    f.write("-" * 60 + "\n")
                    f.write(f"url: {row[0]}\n")
                    f.write(f"username: {row[1]}\n")
                    f.write(f"password: {row[2]}\n")
                    f.write(f"registration_date: {row[5]}\n")

                    u.write(f"{row[1]}\n")
                    p.write(f"{row[2]}\n")

        
# def _export_csv():
#     return

# def _export_json():
#     return

