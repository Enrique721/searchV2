import argparse


class CMDArgumentParser:
    def __init__(self):
        self.parser = self. __argument_parse()
        self.args = self.parser.parse_args()

    # Flag switches
    # Guarda flags booleanas
    def __flags(self):
        cmd_flags = [
            (("-o", "--output"), {
                "help": "Nome do arquivo de saída",
                "action": "store_true"
            }),
            (("-p", "--path"), {
                "help": "Caminho customizado do banco de dados",
                "action": "store_true"
            }),
            (("-d", "--date"), {
                "help": "Filtrar por data (YYYY-MM-DD)",
                "action": "store_true"
            }),
            (("-e", "--email"), {
                "help": "Buscar por email específico",
                "action": "store_true"
            }),
            (("-x", "--password"), {
                "help": "Buscar por senha específica",
                "action": "store_true"
            }),
            (("-g", "--group"), {
                "help": "Nome do grupo de Info stealer",
                "action": "store_true"
            }),
            (("-z", "--compromised-date"), {
                "help": "Data de vazamento",
                "action": "store_true"
            }),
            (("-i", "--include-invalid"), {
                "help": "Incluir credenciais invalidadas no resultado",
                "action": "store_true"
            }),
        ]

        return cmd_flags

    def __argument_parse(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="smarthunter",
            usage="smarthunter [options] <pattern>",
            description="Busca credenciais vazadas no banco de dados"
        )

        cmd_flags = self.__flags()
        for flags, params in cmd_flags:
            parser.add_argument(*flags, **params)

        return parser

    def get_args(self):
        return self.args
