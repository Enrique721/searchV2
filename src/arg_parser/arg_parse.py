import argparse


class CMDArgumentParser:
    def __init__(self):
        self.parser = self. __argument_parse()
        self.args = self.parser.parse_args()
        print(self.args)

    # Flag switches
    # Guarda flags booleanas
    def __flags(self):
        cmd_flags = [
            (("-o", "--output"), {
                "help": "Nome do arquivo de saída",
                "action": "store_true"
            }),
            (("-s", "--url"), {
                "help": "Buscar por email específico",
                "action": "store_true"
            }),
            (("-u", "--username"), {
                "help": "Buscar por email específico",
                "action": "store_true"
            }),
            (("-p", "--password"), {
                "help": "Buscar por senha específica",
                "action": "store_true"
            }),
            (("-t", "--tags"), {
                "help": "Nome do grupo de Info stealer",
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

        parser.add_argument(
            "pattern",
            help="Padrão de busca (email, domínio, hash, etc)"
        )

        return parser

    def get_args(self):
        return self.args
