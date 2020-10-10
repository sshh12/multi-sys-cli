import digitalocean


class PoolProvider:
    def get_pools(self):
        return []

    def get_create_options(self):
        return []

    def create(self, **kwargs):
        pass


class Pool:
    def __init__(self, name, systems):
        self.name = name
        self.systems = systems
        self.size = len(systems)

    def delete(self):
        for system in self.systems:
            system.delete()

    def __repr__(self):
        return f"Pool({self.name}, {self.systems})"
