#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from shutil import copyfile
import apkdiff

BRANCH_KEY = 'GIT_BRANCH'
WORKSPACE_KEY = 'WORKSPACE'
APK_NAME = 'blackfish-debug.apk'
APK_RELATIVE_LOCATION = '/blackfish-android/build/outputs/apk/' + APK_NAME


def get_artifact_dir():
    branch = get_env_value(BRANCH_KEY)
    workspace_dir = get_env_value(WORKSPACE_KEY)
    print 'branch: ' + branch
    print 'workspace: ' + workspace_dir
    artifact_dir = workspace_dir + '/../' + branch
    if not os.path.isdir(artifact_dir):
        os.makedirs(artifact_dir)
    return artifact_dir


def save_build_apk():
    copyfile(get_build_apk(), get_old_apk())


def get_build_apk():
    workspace_dir = get_env_value(WORKSPACE_KEY)
    apk_src = workspace_dir + APK_RELATIVE_LOCATION
    if not os.path.isfile(apk_src):
        raise Exception(apk_src + ' does not exist')
    return apk_src


def get_old_apk():
    return get_artifact_dir() + '/' + APK_NAME


def get_env_value(key=''):
    value = os.environ.get(key)
    if value is None:
        raise Exception('invalid: ' + key)
    return value


def compare_apk():
    old_apk = get_old_apk()
    if not os.path.isfile(old_apk):
        print 'old apk does not exist'
        return
    new_apk = get_build_apk()
    old_file_summary = apkdiff.find_files_size(old_apk, suffix='old')
    new_file_summary = apkdiff.find_files_size(new_apk, suffix='new')
    apkdiff.diff_apks(old_file_summary, new_file_summary)


if __name__ == '__main__':
    compare_apk()
    save_build_apk()
