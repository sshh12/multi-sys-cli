import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Sub Commands", dest="sub_cmd")

    pool_parser = subparsers.add_parser("pool", help="Pool Commands")
    pool_parser.add_argument("pool_cmd", help="pool", choices=("create", "list", "delete", "exec"))
    pool_parser.add_argument("-n", "--name", help="pool name")
    pool_parser.add_argument("-c", "--cmd", help="command")

    return parser.parse_args()