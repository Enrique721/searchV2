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

def _export_row(
    directory: str,
    report_name: str,
    rows: Iterable[sqlite3.Row],
):
    output_path = Path(directory) / report_name

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("SmartHunter Report\n")
        f.write("=" * 18 + "\n")
        f.write(f"Generated at : {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")

        count = 0
        for row in rows:
            status = "INVALID" if not row["valid"] else "VALID"

            f.write("-" * 60 + "\n")
            for key, value in row.items():
                f.write(f"{key.capitalize():<12}: {value}\n")
            f.write(f"Status      : {status}\n")

            count += 1

        f.write("\n")
        f.write(f"Total hits : {count}\n")

        

def _export_cvs():
    return

def _export_json():
    return

