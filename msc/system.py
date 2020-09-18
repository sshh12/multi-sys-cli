import paramiko


class System:
    def delete(self):
        pass

    def get_id(self):
        raise NotImplementedError()

    def get_ip(self):
        raise NotImplementedError()

    def get_pool(self):
        raise NotImplementedError()

    def exec_cmd(self, cmd):
        pool = self.get_pool()
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.get_ip(), username="root", auth_timeout=10)
        stdin, stdout, stderr = client.exec_command(cmd)
        for line in stdout:
            print(f"[{pool.name}-{self.get_id()}]  " + line.strip("\n"))
        client.close()