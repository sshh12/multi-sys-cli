import digitalocean
import threading


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

    def delete(self):
        for system in self.systems:
            system.delete()

    def exec_cmd(self, cmd):
        threads = []
        for system in self.systems:
            thread = threading.Thread(target=system.exec_cmd, args=(cmd,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def __repr__(self):
        return f"Pool({self.name}, {self.systems})"
