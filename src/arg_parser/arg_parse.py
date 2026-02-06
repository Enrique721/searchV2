import argparse

def argument_parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="smarthunter",
        usage="smarthunter [options] <pattern>",
        description="Busca credenciais vazadas no banco de dados"
    )

    # argumento obrigatório
    parser.add_argument(
        "pattern",
        help="Padrão de busca (email, senha ou regex)",
        required=True
    )

    # opções
    parser.add_argument(
        "-o", "--output",
        help="Nome do arquivo de saída"
    )

    parser.add_argument(
        "-p", "--path",
        help="Caminho customizado do banco de dados"
    )

    parser.add_argument(
        "-d", "--date",
        help="Filtrar por data (YYYY-MM-DD)"
    )

    parser.add_argument(
        "-e", "--email",
        help="Buscar por email específico"
    )

    parser.add_argument(
        "-x", "--password",
        help="Buscar por senha específica"
    )

    parser.add_argument(
        "-g", "--group",
        help="Nome do grupo de Info stealer"
    )

    parser.add_argument(
        "-z", "--compromised-date",
        help="Data de vazamento" 
    )

    parser.add_argument(
        "-i", "--include-invalid",
        action="store_true",
        help="Incluir credenciais invalidadas no resultado"
    )

    return parser
