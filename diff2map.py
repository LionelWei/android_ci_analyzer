#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import sys
import string

map_old = {}
map_new = {}
map_result = {}

FILE_THRESHOLD = 1024


def diff2html(f):
    with open('tst.html', 'wb') as html_file:
        with open('./diff_csv.csv', 'rb') as csv_file:
            table_string = ""
            reader = csv.reader(csv_file)
            for row in reader:
                table_string += "<tr>" + \
                                "<td>" + \
                                string.join(row, "</td><td>") + \
                                "</td>" + \
                                "</tr>\n"
            print table_string
            html_file.write(table_string)


def diff2map(f, debug=False):
    if not os.path.isfile(f):
        raise Exception(f + ' does not exist')
    with open(f) as in_file:
        for line in in_file:
            arr = line.rstrip().split(' ')
            if len(arr) != 2:
                continue
            k, v = arr
            if k.startswith('-') and not k.startswith('--'):
                map_old[v] = k[1:]
            elif k.startswith('+') and not k.startswith('++'):
                map_new[v] = k[1:]
    for k, v in map_new.items():
        if k not in map_old:
            increment = int(v)
        else:
            increment = int(v) - int(map_old[k])
        if increment > FILE_THRESHOLD:
            map_result[k] = increment
    for k, v in map_result.items():
        print k, v
    zipped_result = zip(map_result.keys(), map_result.values())
    with open('./diff_csv.csv', 'wb') as f:
        out = sys.stderr if debug else f
        w = csv.writer(out)
        for row in zipped_result:
            w.writerow(row)


if __name__ == '__main__':
    # diff2map('./result.txt', debug=True)
    diff2map('./diff_result.txt')
