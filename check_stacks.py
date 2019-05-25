#!/usr/bin/env python3

from pathlib import Path
from yaml import safe_load
#import operator
import itertools

def flatten(lol):
    return(list(itertools.chain(*lol)))

def read_stacks():
    stacks = {}
    for stack_yaml in Path('stacks').glob('**/stack.yml'):
        with open(stack_yaml, 'r') as f:
            stack = safe_load(f.read())
            stacks[str(stack_yaml)] = stack

    return(stacks)

def get_dupes(l):
    return([x for n, x in enumerate(l) if x in l[:n]])

if __name__=="__main__":
    stacks = read_stacks()

    # check for stack names intersections
    names = list(map (lambda x: stacks[x]['name'], stacks.keys()))
    dupes = get_dupes(names)
    if dupes:
        print("[WARNING]: stacks with same names")
        dup_stacks = []
        for n in dupes:
            dup_stacks = [(stacks[x]['name'], x) for x in stacks.keys() if stacks[x]['name'] in dupes]

        dup_stacks.sort()

        for s in dup_stacks:
            print("\t{}".format(s))

    # check if priv nets is intersects
    priv_vlans = {}
    for f,s in stacks.items():
        stack = s['name']
        for node in s['nodes']:
            priv_vlans[f] = []
            for iface, params in s['nodes'][node]['net'].items():
                if "descr" in params.keys() and params["descr"] == "priv":
                    priv_vlans[f].append((params['tag'],node,iface,stack))

            dupes = get_dupes(priv_vlans[f])
            if dupes:
                print("[ERROR] node {} in {} stack has more than one inerface with same VLAN tag {}".format(node,stack,dupes[0]))

    all_priv_tags = []
    for k,v in priv_vlans.items():
        all_priv_tags.append([x[0] for x in v])
#        print("{}\t{}".format(v,k))

    dupes = get_dupes(flatten(all_priv_tags))
    if dupes:
        dup_tags = {}
        for d in dupes:
            dup_tags[d] = ([(k,v) for k,v in priv_vlans.items() if d in [t[0] for t in v]])
        print("\n[WARNING] this priv nets has a same VLAN in different stacks")
        for t,ss in dup_tags.items():
            stacks = [x[0] for x in ss]
            print("\t{}\t{}\n".format(t,'\n\t\t'.join(stacks)))

#f1 = open("./stacks/demo-samba-sisyphus-3x3/stack.yml")
