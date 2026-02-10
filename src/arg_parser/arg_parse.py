import argparse


class CMDArgumentParser:
    def __init__(self):
        self.parser = self. __argument_parse()
        self.args = self.parser.parse_args()

    # Flag switches
    # Guarda flags e as respectivas flags
    def __flags(self):
        cmd_flags = [
            (("-o", "--output"), {
                "help": "Nome do arquivo de saída",
            }),
            (("-s", "--url"), {
                "help": "Buscar por url específica",
                "action": "store_true"
            }),
            (("-u", "--username"), {
                "help": "Buscar por usuário/email/número de celular/etc específico",
                "action": "store_true"
            }),
            (("-p", "--password"), {
                "help": "Buscar por senha específica",
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

        # Argumento de tag
        parser.add_argument( "-t", "--tag", help="Tags de busca t1,t2,t3", type= lambda s: s.split(","))
        parser.add_argument( "pattern", help="Padrão de busca (email, domínio, hash, etc)" )

        return parser

    def get_args(self):
        return self.args
