#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Sergey Bubnov (@homgbebebe) <omg at altlinux.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = r'''
---
module: proxmox_qemu_agent
short_description: Execute qemu-agent commands on Qemu(KVM) Virtual Machines in Proxmox VE cluster.
description:
  - Allows you to execute qemu-agent command on virtual machines
version_added: "2.6"
author: "Sergey Bubnov (@homgbebebe) <omg at altlinux.org>"
options:
  api_host:
    description:
      - Specify the target host of the Proxmox VE cluster.
    required: true
  api_user:
    description:
      - Specify the user to authenticate with.
    required: true
  api_password:
    description:
      - Specify the password to authenticate with.
      - You can use C(PROXMOX_PASSWORD) environment variable.
  name:
    description:
      - Specifies the VM name.
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    type: bool
    default: 'no'
  vmid:
    description:
      - Specifies the VM ID. Instead use I(name) parameter.
requirements: [ "proxmoxer", "requests" ]
'''

EXAMPLES = '''
# Ping VM via agent interface
- proxmox_qemu_agent:
    api_user    : root@pam
    api_password: secret
    api_host    : helldorado
    name        : vm1
    commnad     : ping
'''

RETURN = '''
'''

import os
import re
import time
import traceback

try:
    from proxmoxer import ProxmoxAPI
    HAS_PROXMOXER = True
except ImportError:
    HAS_PROXMOXER = False

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


VZ_TYPE = 'qemu'


def get_vmid(proxmox, name):
    return [vm['vmid'] for vm in proxmox.cluster.resources.get(type='vm') if vm['name'] == name]


def get_vm(proxmox, vmid):
    return [vm for vm in proxmox.cluster.resources.get(type='vm') if vm['vmid'] == int(vmid)]


def agent_command(module, proxmox, vm, vmid, command):
    try:
        r = getattr(proxmox.nodes(vm[0]['node']), VZ_TYPE)(vmid).agent.post(command=command)
        module.exit_json(changed=False, results=r['result'])
    except Exception as e:
        module.fail_json(msg='qemu-agent request failed withexception: %s' % e)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_host=dict(required=True),
            api_user=dict(required=True),
            api_password=dict(no_log=True),
            name=dict(type='str'),
            command=dict(default=None, choices=
                         ['ping', 'get-time', 'info', 'fsfreeze-status', 'fsfreeze-freeze', 'fsfreeze-thaw', 'fstrim'
                          ,'network-get-interfaces', 'get-vcpus', 'get-fsinfo', 'get-memory-blocks', 'get-memory-block-info'
                          ,'suspend-hybrid', 'suspend-ram', 'suspend-disk', 'shutdown'
                         ]),
            validate_certs=dict(type='bool', default='no'),
            vmid=dict(type='int', default=None),
        ),
        required_one_of=[('name', 'vmid',)],
    )

    if not HAS_PROXMOXER:
        module.fail_json(msg='proxmoxer required for this module')

    api_user = module.params['api_user']
    api_host = module.params['api_host']
    api_password = module.params['api_password']
    command = module.params['command']
    name = module.params['name']
    vmid = module.params['vmid']
    validate_certs = module.params['validate_certs']

    # If password not set get it from PROXMOX_PASSWORD env
    if not api_password:
        try:
            api_password = os.environ['PROXMOX_PASSWORD']
        except KeyError as e:
            module.fail_json(msg='You should set api_password param or use PROXMOX_PASSWORD environment variable')

    try:
        proxmox = ProxmoxAPI(api_host, user=api_user, password=api_password, verify_ssl=validate_certs)
        global VZ_TYPE
        global PVE_MAJOR_VERSION
        PVE_MAJOR_VERSION = 3 if float(proxmox.version.get()['version']) < 4.0 else 4
    except Exception as e:
        module.fail_json(msg='authorization on proxmox cluster failed with exception: %s' % e)

    # If vm name is set get the VM id from ProxmoxAPI
    if not vmid:
        try:
            vmid = get_vmid(proxmox, name)[0]
            if vmid:
                vm = get_vm(proxmox, vmid)
                if not vm:
                    module.fail_json(msg='VM with vmid = %s does not exist in cluster' % vmid)
        except Exception as e:
            module.fail_json(msg="VM {} does not exist in cluster.".format(clone))

    agent_command(module, proxmox, vm, vmid, command)


if __name__ == '__main__':
    main()
