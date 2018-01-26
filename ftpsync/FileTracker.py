# -*- coding: utf-8 -*-

import struct
import os
import hashlib

class FileTracker:
    """
    文件追踪器，用于判断文件是否是最新版
    """

    def __init__(self):
        self.data = dict()

    def load(self, filename):
        self.data = dict()
        with open(filename, 'rb') as fp:
            while True:
                filename_md5 = fp.read(16)
                if not filename_md5:
                    break
                modify_time = struct.unpack('I', fp.read(4))[0]
                self.data[filename_md5] = modify_time

    def save(self, filename):
        with open(filename, 'wb') as fp:
            for filename_md5, modify_time in self.data.items():
                fp.write(filename_md5)
                fp.write(struct.pack('I', modify_time))

    def add(self, filename):
        modify_time = int(os.path.getmtime(filename))
        md5 = hashlib.md5()
        md5.update(filename)
        filename_md5 = md5.digest()
        if filename_md5 in self.data and self.data[filename_md5] == modify_time:
            return False
        self.data[filename_md5] = modify_time
        return True

    def is_new(self, filename):
        return self.is_new_added(filename) or not self.is_old(filename)

    def is_old(self, filename):
        modify_time = int(os.path.getmtime(filename))
        md5 = hashlib.md5()
        md5.update(filename)
        filename_md5 = md5.digest()
        return filename_md5 in self.data and self.data[filename_md5] == modify_time

    def is_new_added(self, filename):
        md5 = hashlib.md5()
        md5.update(filename)
        filename_md5 = md5.digest()
        return filename_md5 not in self.data
