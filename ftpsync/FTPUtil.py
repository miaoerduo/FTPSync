# -*- coding: utf-8 -*-

import ftplib


class FTP:

    def __init__(self, host, user, password, timeout=None):
        self.ftp = ftplib.FTP(host=host, user=user, passwd=password, timeout=timeout)

    def upload(self, local_path, remote_path):
        with open(local_path, 'rb') as fp:
            self.ftp.storbinary('STOR {}'.format(remote_path), fp)

