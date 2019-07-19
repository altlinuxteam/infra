"""Configuration for pytest runner."""

from pytest_bdd import given, when
import pytest
import paramiko
from paramiko.config import SSHConfig
from os.path import expanduser
import sys
import os
import inspect

pytest_plugins = "pytester"
cvet = {}

SSH_USERNAME = os.getenv("SSH_USERNAME", "root")

class Target:
    def __init__(self, host):
        self.host = host
        config_file = open(expanduser('.tmp/ssh_config'))
        config = SSHConfig()
        config.parse(config_file)
        ip = config.lookup(host).get('hostname', None)
        port = config.lookup(host).get('port', 22)
        pk = config.lookup(host).get('identityfile', None)

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=ip, port=int(port), username=SSH_USERNAME, key_filename=pk)
        s = self.ssh.get_transport().open_session()
        paramiko.agent.AgentRequestHandler(s)
    def __exit__(self):
        self.ssh.close()

    def exec_command(self, cmd):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        self.res =  {'rc': ssh_stdout.channel.recv_exit_status(),
                     'cmd': cmd,
                     'host': self.host,
                     'stdout': ssh_stdout.read(),
                     'stderr': ssh_stderr.read()}
        return self.res


@given("I have a root fixture")
def root():
    return "root"


@when("I use a when step from the parent conftest")
def global_when():
    pass


def assert_cmd(expect, res):
    assert expect(res), "execution of '{}' failed on '{}' with '{}'; lambda is: {}".format(res['cmd'], res['host'], res['stdout'] + res['stderr'], inspect.getsource(expect))


def read_env_vars():
    req_vars = ['CVET_ABUSER_NODE',
                'CVET_ABUSER_USER',
                'CVET_ABUSER_USER_WITH_SUDO',
                'CVET_VICTIM_NODE',
                'CVET_VICTIM_NODE_SHORT',
                'CVET_VICTIM_ADDRESS',
                'CVET_ABUSERS',
                'CVET_VICTIMS',
                'CVET_SRC_NIC',
                'CVET_CVE',
                'CVET_TTL',
                'CVET_SRC_START_ADDRESS_RANGE',
                'CVET_SRC_END_ADDRESS_RANGE'
               ]
    list_vars = ['CVET_ABUSERS'
                 'CVET_VICTIMS'
                ]

    for v in req_vars:
        if v not in os.environ:
            print('{} required but is not set'.format(v))
            sys.exit(1)
        cvet[v.split('_',1)[1].lower()] = os.environ[v] if v not in list_vars else filter(None, os.environ[v].split(' '))
    cvet['all_hosts'] = cvet['abusers'] + cvet['victims']
read_env_vars()

@pytest.fixture(scope='session', params=cvet['all_hosts'])
def ssh_all(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=[cvet['abuser_node']])
def ssh_abuser(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=[cvet['victim_node']])
def ssh_victim(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=cvet['abusers'])
def ssh_abusers(request):
    return Target(request.param)

@pytest.fixture(scope='session', params=cvet['victims'])
def ssh_victims(request):
    return Target(request.param)

@pytest.fixture(scope='session')
def cvet_params():
    return cvet
