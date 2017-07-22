#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import zipfile
from diff2map import diff2map


diff_file = ''


def unzip_file(f):
    check_file(f)
    zip_ref = zipfile.ZipFile(f, 'r')
    dst = os.path.dirname(os.path.abspath(f)) + '/' + os.path.basename(f).split('.')[0]
    print f + ' ' + dst
    if not os.path.exists(dst):
        os.makedirs(dst)
    zip_ref.extractall(dst)
    zip_ref.close()
    return dst


def check_file(f=''):
    if not os.path.exists(f):
        print f + ' does not exist'
        exit(0)


def calculate_dex_size(f):
    exec_cmd = "cd %s; ls -l `find . -name '*.dex'` | awk '{print $5}' | awk '{sum+=$NF} END {print sum}'" % f
    dex_size = os.popen(exec_cmd).read()
    os.system("cd %s; rm *.dex" % f)
    print 'dex_size: ' + dex_size
    return dex_size.rstrip()


def find_files_size(f):
    check_file(f)
    unzipped = unzip_file(f)
    if not os.path.isdir(unzipped):
        raise Exception(unzipped + ' is not directory')
    output = os.path.abspath(unzipped) + '/../' + os.path.basename(unzipped).split('.')[0] + ".txt"
    print 'output ' + output
    out_file = open(output, 'w')
    out_file.close()
    dex_size = calculate_dex_size(unzipped)
    exec_cmd = "cd %s; find . -type f | sort | xargs ls -l| awk '{print $5,$9}' > %s; cd ..;" % (unzipped, output)
    print exec_cmd
    os.system(exec_cmd)
    with open(output, "a") as result_file:
        result_file.write(str(dex_size) + ' ./dex\n')
    return output


def diff_apks(f1, f2):
    global diff_file
    cur_dir = os.path.dirname(os.path.abspath(f1))
    diff_file = cur_dir + '/diff_result.txt'
    exec_cmd = "git diff --no-index %s %s > %s" % (f1, f2, diff_file)
    os.system(exec_cmd)


def main():
    arg_len = len(sys.argv)

    if arg_len != 3:
        print "参数有误"
        exit(0)

    file1 = sys.argv[1]
    result1 = find_files_size(file1)
    file2 = sys.argv[2]
    result2 = find_files_size(file2)
    diff_apks(result1, result2)
    diff2map(diff_file)


if __name__ == '__main__':
    main()
