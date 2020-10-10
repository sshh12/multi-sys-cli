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

    def get_default_user(self):
        return "root"

    def get_paramiko_ssh_client(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return client