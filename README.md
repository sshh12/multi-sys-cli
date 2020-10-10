# multi-sys-cli (`msc`)

> A hassle-free method of SSHing into multiple machines simultaneously.

## Install

```
$ pip install git+https://github.com/sshh12/multi-sys-cli
$ msc --help
```

For Digital Ocean, set the environment variable: `DIGITALOCEAN_ACCESS_TOKEN=6afa9a...your api key...`.

## Usage

### Create a Pool

```
$ msc pool create
? What provider do you want to use?  digitalocean
? Pool name?  webscraping
? How many systems?  10
? Confirm?  Yes
```

### Run a Distributed Command

Execute a given command on all machines in the `webscraping` pool.

```
$ msc pool exec --name webscraping --cmd "ls /"
[webscraping-0]  bin
[webscraping-0]  boot
[webscraping-0]  dev
...
[webscraping-1]  bin
[webscraping-1]  boot
[webscraping-1]  dev
...
```

### Interactive Multi-Shell

Execute the given command on all the machine in the `webscraping` pool.

```
$ msc pool shell
? Pool name  webscraping
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-45-generic x86_64)
...
root@msc-webscraping-0:~#
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-45-generic x86_64)
...
root@msc-webscraping-1:~#
```
