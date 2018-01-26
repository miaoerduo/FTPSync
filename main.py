# -*- coding: utf-8 -*-

import argparse
import json
import ftplib
import os
import ftpsync
import sys

reload(sys)  
sys.setdefaultencoding('utf8')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="------ FTP Sync ------")
    parser.add_argument('-c',  type=str)
    args = parser.parse_args()
    with open(args.c) as fp:
        config = json.load(fp)

    host = config.get('host')
    user = config.get('user')
    password = config.get('password')
    local_root = config.get('local_root')
    remote_root = config.get('remote_root')
    timeout = config.get('timeout', None)
    ignore = config.get('ignore', None)
    track = config.get('track', None)

    file_ignore_util = ftpsync.FileIgnoreUtil()
    if ignore:
        if os.path.exists(ignore):
            file_ignore_util.set_ignore(ignore)

    file_tracker = ftpsync.FileTracker()
    if track:
        track = os.path.abspath(track)
        if os.path.exists(track):
            file_tracker.load(track)

    ftp = ftpsync.FTP(host, user, password, timeout)
    os.chdir(local_root)

    for root, _, filenames in os.walk('.'):
        for filename in filenames:
            filename_full = os.path.normpath(os.path.join(root, filename))
            if filename_full in file_ignore_util:
                continue
            if file_tracker.is_new(filename_full):
                with open(filename_full, 'rb') as fp:
                    try:
                        print("upload: {}".format(filename_full))
                        ftp.upload(filename_full, os.path.join(remote_root, filename_full))
                        file_tracker.add(filename_full)
                    except Exception as e:
                        print(e)
                        print('cannot upload: {}'.format(filename_full))
    if track:
        file_tracker.save(track)
