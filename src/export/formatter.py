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
    export_type: str = "row",
):

    if export_type == "row":
        _export_row(directory=directory, report_name=report_name + ".txt", rows=query_result)

# ('https://enrollapp.com', 'rania.nsairat@gmail.com', '0799352708rayan', None, None, '2026-02-10T15:05:51.268511', None)
def _export_row(
    directory: str,
    report_name: str,
    rows: List[Tuple],
):
    output_path = Path(directory) / report_name

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("SmartHunter Report\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated at : {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
        f.write("=" * 60 + "\n")

        count = 0

        if len(rows) == 0:
            f.write("-" * 60 + "\n")
            f.write("Nada foi encontrado")
            f.write("XP")
            f.write("-" * 60 + "\n")
            return
#
#
# url, username, password, group_id, compromised_date, registration_date, access_date
# 
        for row  in rows:
            f.write("-" * 60 + "\n")
            f.write(f"url: {row[0]}\n")
            f.write(f"username: {row[1]}\n")
            f.write(f"password: {row[2]}\n")
            f.write(f"registration_date: {row[5]}\n")
            count += 1

        f.write("\n")
        f.write(f"Total hits : {count}\n")

        

def _export_cvs():
    return

def _export_json():
    return

