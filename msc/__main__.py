import paramiko
from PyInquirer import prompt
from msc.args import parse_args
from msc.digitalocean import DigitalOceanPoolProvider


def pool_list(provs):
    pools = []
    for provider in provs:
        pools.extend(provider.get_pools())
    for pool in pools:
        print(pool.name, pool.systems)


def pool_create(provs):
    prov_name = prompt(
        [
            {
                "type": "rawlist",
                "name": "provider",
                "message": "What provider do you want to use?",
                "choices": [prov.name for prov in provs],
            }
        ]
    )["provider"]
    prov = [prov for prov in provs if prov.name == prov_name][0]
    ans = prompt(prov.get_create_options())
    confirm = prompt([{"type": "confirm", "name": "confirm", "message": "Confirm?", "default": False}])["confirm"]
    if not confirm:
        return
    prov.create(**ans)


def get_pool_by_name(provs, name):
    for provider in provs:
        for pool in provider.get_pools():
            if pool.name == name:
                return pool
    raise Exception()


def pool_delete(provs, name):
    pool = get_pool_by_name(provs, name)
    pool.delete()


def pool_exec(provs, name, cmd=None):
    pool = get_pool_by_name(provs, name)
    if cmd is None:
        cmd = prompt([{"type": "input", "name": "cmd", "message": "Command"}])["cmd"]
    pool.exec_cmd(cmd)


def main():
    providers = [DigitalOceanPoolProvider()]

    args = parse_args()
    # print(args)
    if args.sub_cmd == "pool":
        if args.pool_cmd == "list":
            pool_list(providers)
        elif args.pool_cmd == "create":
            pool_create(providers)
        elif args.pool_cmd == "delete":
            pool_delete(providers, args.name)
        elif args.pool_cmd == "exec":
            pool_exec(providers, args.name, args.cmd)


if __name__ == "__main__":
    main()
    sys.exit(0)