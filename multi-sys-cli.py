import paramiko
from PyInquirer import prompt
from msc.args import parse_args
from msc.pool import DigitalOceanPoolProvider


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


if __name__ == "__main__":
    providers = [DigitalOceanPoolProvider()]

    args = parse_args()
    print(args)
    if args.sub_cmd == "pool":
        if args.pool_cmd == "list":
            pool_list(providers)
        elif args.pool_cmd == "create":
            pool_create(providers)

# droplet = digitalocean.Droplet(name='api-example',
#                                region='sfo2',
#                                image='ubuntu-20-04-x64',
#                                size_slug='s-1vcpu-1gb',
#                                ssh_keys=keys,
#                                backups=False)
# droplet.create()
# asdasd

# droplet.load()
# droplet.ip_address
# import sys
# import threading
# def windows_shell(chan1, chan2):
#     def writeall(sock, name):
#         while True:
#             data = sock.recv(256)
#             if not data:
#                 sys.stdout.write("\r\n*** EOF ***\r\n\r\n")
#                 sys.stdout.flush()
#                 break
#             text = str(data, "ascii")
#             text = text.replace("\n", "\n[{}]".format(name))
#             sys.stdout.write(text)
#             sys.stdout.flush()

#     writer = threading.Thread(target=writeall, args=(chan1, "a"))
#     writer.start()
#     writer2 = threading.Thread(target=writeall, args=(chan2, "b"))
#     writer2.start()

#     try:
#         while True:
#             d = sys.stdin.read(1)
#             if not d:
#                 break
#             chan1.send(d)
#             chan2.send(d)
#     except EOFError:
#         pass
# def get_client():
#     client = paramiko.SSHClient()
#     client.load_system_host_keys()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect('138.197.195.31', username="root", auth_timeout=10)
#     return client
# c1 = get_client()
# c2 = get_client()
# chan1 = c1.invoke_shell()
# chan2 = c1.invoke_shell()
# windows_shell(chan1, chan2)
# chan1.close()
# chan2.close()
# c1.close()
# c2.close()