import argparse
from PyInquirer import prompt


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Sub Commands", dest="sub_cmd")

    pool_parser = subparsers.add_parser("pool", help="Pool Commands")
    pool_parser.add_argument("pool_cmd", help="pool", choices=("create", "list", "delete", "exec", "shell"))
    pool_parser.add_argument("-n", "--name", help="pool name")
    pool_parser.add_argument("-c", "--cmd", help="command")

    return parser.parse_args()


def prompt_string_arg_if_none(value, name):
    if value is None:
        return prompt([{"type": "input", "name": "x", "message": name}])["x"]
    return value