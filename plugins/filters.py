#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.listify import listify_lookup_plugin_terms
import collections
import re
import ipaddress

try:
    import jmespath
    HAS_LIB = True
except ImportError:
    HAS_LIB = False

def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def dict_inject(data, path, obj):
    p = path.split('/')
    p.remove('')
    p.reverse()
    c = obj
    for n in p:
        c = {n: c}
    z = data.copy()
    dict_merge(z, c)
    return z


def to_nics_dict(src):
    nics = {}
    lo_pat = re.compile("^lo[0-9]{0,2}$")
    for n in src:
        if not lo_pat.match(n['name']):
            addrs = []
            if "ip-addresses" in n:
                for a in n['ip-addresses']:
                    if a['ip-address-type'] != "ipv6":
                        addrs.append(u'%s/%s' % (a['ip-address'], a['prefix']))
            nics[n['name']] = {"mac": n['hardware-address'],
                               "addrs": addrs}
    return nics

def to_proxmox_net(src):
    out = {}
    ks = ['virtio', 'bridge', 'tag']
    for k,v in src.items():
        k = k.replace('eth','net')
        [ v.pop(x, None) for x in set(v.keys()).difference(ks) ]
        v.pop('ipv4', None) # remove unused key
        if 'virtio' not in v.items():
            res = "virtio,"
        else:
            res = ""
        res = res + ','.join(map(lambda x:str('='.join(map(str,x))), v.items()))
        out[k] = res
    return out

def gen_nics_addrs(node, num):
    res = node.copy()
    for k, v in res['net'].items():
        for i, a in enumerate(res['net'][k]['ipv4']):
            interface = ipaddress.ip_interface(a)
            addr = interface.ip + int(num)
            cidr = interface.network.prefixlen
            res['net'][k]['ipv4'][i] = '%s/%s' % (addr, cidr)
    return res

def list_to_dict(src):
    res = {}
    for a in src:
        k = list(a.keys())[0]
        res[k] = a[k]
    return res

def get_steps(node, steps_list):
    res = []
    for idx, ss in enumerate(steps_list):
        for a in ss:
            if node in a['binds']:
                res.append("step%s" % idx)
    return res

def filter_dict(src, pred):
    p = eval(pred)
    return { k: v for k, v in src.iteritems() if p(v)}

class FilterModule(object):
    ''' Query filter '''
    def filters(self):
        return {
            'dict_merge': dict_merge,
            'dict_inject': dict_inject,
            'to_nics_dict': to_nics_dict,
            'to_proxmox_net': to_proxmox_net,
            'gen_nics_addrs': gen_nics_addrs,
            'list_to_dict': list_to_dict,
            'get_steps': get_steps,
            'filter_dict': filter_dict
        }
