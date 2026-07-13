from src.file_ops.file_operation import DirectoryOperation
from src.db.db_query_builder import QueryBuilder
from src.db.db_operation import DatabaseOperation
from src.db.db_connection import DatabaseConnection
from src.arg_parser.arg_parse import CMDArgumentParser
from src.export.formatter import make_directory, export_data

import sys

def main():
    parser_object = CMDArgumentParser()
    args = parser_object.get_args()

    db_connection = DatabaseConnection()

    db_executor = DatabaseOperation(
                        db_connection,
                        query_builder=QueryBuilder()
                    )

    if len(args.pattern) == 1 and args.pattern == '/':
        print("Invalid query param")
        return

    print(f"Iniciando a busca por credenciais com a substring: {args.pattern}")
    query_result = db_executor.query_executor_search(
        url=args.url,
        username=args.username,
        # Não esta sendo usado,
        # se precisar avisar
        # password=args.password, 
        pattern=args.pattern,
        tags=args.tag
    )

    print("Conclusão da busca.")


    print("Criando diretório.")
    directory_operation = DirectoryOperation()
    directory = directory_operation.create_directory(
                         args.output if args.output else args.pattern
                     )
    print("Diretório criado.")

    print("Escrevendo o relatório")
    export_data(
        directory=str(directory),
        report_name=args.output if args.output else args.pattern,
        query_result=query_result,
        pattern=args.pattern
    )
    print("Relatório escrito")

    db_connection.closeConnection()
    
if __name__ == "__main__":
    main()
