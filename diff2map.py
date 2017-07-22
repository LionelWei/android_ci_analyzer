#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

map_old = {}
map_new = {}
map_result = {}


def diff2map(f):
    if not os.path.isfile(f):
        raise Exception(f + ' does not exist')
    with open(f) as in_file:
        for line in in_file:
            k, v = line.rstrip().split(' ')
            if k.startswith('-'):
                map_old[v] = k[1:]
            elif k.startswith('+'):
                map_new[v] = k[1:]
    for k, v in map_new.items():
        if k in map_old:
            increment = int(v) - int(map_old[k])
            map_result[k] = increment
    for k, v in map_result.items():
        print k, v

if __name__ == '__main__':
    diff2map('./result.txt')
