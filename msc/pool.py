import digitalocean
from collections import defaultdict


class PoolProvider:
    pass


class Pool:
    def __init__(self, name, systems):
        self.name = name
        self.systems = systems

    def __repr__(self):
        return f"Pool({self.name}, {self.systems})"


class System:
    pass


class DigitalOceanSystem(System):
    def __init__(self, droplet):
        self.droplet = droplet
        self.id = int(self.droplet.name.split("-")[-1])
        self.ip = self.droplet.ip_address

    def __repr__(self):
        return f"System({self.id}, {self.ip})"


class DigitalOceanPoolProvider(PoolProvider):
    def __init__(self):
        self.name = "digitalocean"
        self.manager = digitalocean.Manager()
        self.keys = self.manager.get_all_sshkeys()

    def get_pools(self):
        # msc-{pool}-{id}
        droplets = self.manager.get_all_droplets()
        pools = defaultdict(list)
        for droplet in droplets:
            name = droplet.name
            if not name.startswith("msc"):
                continue
            name_split = name.split("-")
            pool_id = "-".join(name_split[1:-1])
            pools[pool_id].append(DigitalOceanSystem(droplet))
        return [Pool(pool_id, sys) for pool_id, sys in pools.items()]

    def get_create_options(self):
        return [
            {
                "type": "input",
                "name": "name",
                "message": "Pool name?",
            },
            {
                "type": "input",
                "name": "count",
                "message": "How many systems?",
                "filter": (lambda val: int(val)),
            },
        ]

    def create(self, name="new-pool", count=1):
        for i in range(count):
            droplet = digitalocean.Droplet(
                name=f"msc-{name}-{i}",
                region="sfo2",
                image="ubuntu-20-04-x64",
                size_slug="s-1vcpu-1gb",
                ssh_keys=self.keys,
                backups=False,
            )
            droplet.create()
