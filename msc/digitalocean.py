import digitalocean
from collections import defaultdict
from msc.pool import PoolProvider, Pool
from msc.system import System


class DigitalOceanSystem(System):
    def __init__(self, droplet):
        self.droplet = droplet
        self.id = int(self.droplet.name.split("-")[-1])
        self.ip = self.droplet.ip_address

    def get_ip(self):
        return self.ip

    def get_pool(self):
        return self.pool

    def get_id(self):
        return self.id

    def delete(self):
        self.droplet.destroy()

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
        do_pools = []
        for pool_id, systems in pools.items():
            do_pools.append(Pool(pool_id, systems))
        return do_pools

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