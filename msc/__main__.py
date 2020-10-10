from msc.args import parse_args, prompt_string_arg_if_none
from msc.pool_cmds import pool_list, pool_create, pool_delete, pool_exec, pool_shell
from msc.digitalocean import DigitalOceanPoolProvider


def main():
    providers = [DigitalOceanPoolProvider()]

    args = parse_args()

    if args.sub_cmd == "pool":
        if args.pool_cmd == "list":
            pool_list(providers)
        elif args.pool_cmd == "create":
            pool_create(providers)
        elif args.pool_cmd == "delete":
            name = prompt_string_arg_if_none(args.name, "Pool name")
            pool_delete(providers, name)
        elif args.pool_cmd == "exec":
            name = prompt_string_arg_if_none(args.name, "Pool name")
            pool_exec(providers, name, args.cmd)
        elif args.pool_cmd == "shell":
            name = prompt_string_arg_if_none(args.name, "Pool name")
            pool_shell(providers, name)


if __name__ == "__main__":
    main()