import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="Sub Commands", dest="sub_cmd")

    pool_parser = subparsers.add_parser("pool", help="...")
    pool_methods = pool_parser.add_mutually_exclusive_group()
    pool_methods.add_argument("pool_cmd", help="run or stop", nargs="?", choices=("create", "list"))

    return parser.parse_args()