# Samba DC testing infrastructure deployment


## Contents

* [Prerequisites](#prerequisites)
* [Quickstart](#quickstart)

* * *


## Prerequisites

* Ansible with necessary Python modules installed;
* Git with git-subtree module installed.


## Quickstart

install prerequired ansible 2.6+ and python modules
```sh
apt-get install ansible \
    python-module-proxmoxer \
    python-module-jmespath \
    python-module-netaddr \
    git-subtree
```

init submodules and pull infra-conf repository
```sh
export CONF_URI="http://gogs.srt/BaseALT/infra-conf.git"
git submodule update --init --recursive
git subtree add --prefix=vars/conf "${CONF_URI}" master
ssh-add ~/.ssh/robot_key
```

do not forget to add robot ssh-key and clone passdb

deploy desired stack
```sh
./infra.sh test-env test-stack
```
