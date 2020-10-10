import paramiko
import threading
import queue
import sys
from PyInquirer import prompt


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
        while cmd != "":
            _exec_cmd(pool, cmd)
            cmd = prompt([{"type": "input", "name": "cmd", "message": "Command"}])["cmd"]
    else:
        _exec_cmd(pool, cmd)


def pool_shell(provs, name):
    pool = get_pool_by_name(provs, name)
    _exec_shell(pool)


def _insert_string_vars(system, pool, cmd):
    return cmd.replace("{{pool_idx}}", str(system.get_id())).replace("{{pool_size}}", str(pool.size))


def _exec_cmd(pool, cmd):
    def ssh_and_exec(system, client, cmd):
        client.connect(system.get_ip(), username=system.get_default_user(), auth_timeout=10)
        _, stdout, _ = client.exec_command(cmd)
        for line in stdout:
            print(f"[{pool.name}-{system.get_id()}]  " + line.strip("\n"))
        client.close()

    threads = []
    for system in pool.systems:
        client = system.get_paramiko_ssh_client()
        actual_cmd = _insert_string_vars(system, pool, cmd)
        thread = threading.Thread(target=ssh_and_exec, args=(system, client, actual_cmd))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


def _exec_shell(pool):
    def open_shell(i, system, client, q):
        client.connect(system.get_ip(), username=system.get_default_user(), auth_timeout=10)
        chan = client.invoke_shell()

        def write_all(sock):
            while run_bp[i]:
                data = sock.recv(256)
                if not data:
                    sys.stdout.flush()
                    break
                sys.stdout.write(str(data, "utf-8"))
                sys.stdout.flush()

        writer = threading.Thread(target=write_all, args=(chan,))
        writer.start()

        while run_bp[i]:
            chan.send(_insert_string_vars(system, pool, q.get()))
            q.task_done()

        writer.join()

    queues = []
    threads = []
    run_bp = []
    for i, system in enumerate(pool.systems):
        run_bp.append(True)
        q = queue.Queue()
        client = system.get_paramiko_ssh_client()
        thread = threading.Thread(target=open_shell, args=(i, system, client, q))
        thread.start()
        queues.append(q)
        threads.append(thread)

    try:
        while True:
            user_input = sys.stdin.readline()
            if not user_input:
                break
            for q in queues:
                q.put(user_input)
    except KeyboardInterrupt:
        for i, thread in enumerate(threads):
            run_bp[i] = False
            thread.join()