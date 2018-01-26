# -*- coding: utf-8 -*-

import os


class FileIgnoreUtil:
    """
    文件忽略系统
    """

    FILE = 'file'
    FOLDER = 'folder'
    PREFIX = 'prefix'
    SUFFIX = 'suffix'

    def __init__(self):
        self.filename = None
        self.ignore_dict = None

    def set_ignore(self, filename):
        self.filename = filename
        if not filename:
            return

        _ignore_dict = {
            FileIgnoreUtil.FILE: [],
            FileIgnoreUtil.FOLDER: [],
            FileIgnoreUtil.PREFIX: [],
            FileIgnoreUtil.SUFFIX: []
        }

        with open(filename) as f:
            for line in f:
                data = line.strip()
                if not data:
                    continue
                elif data[0] == '#':
                    # 注释
                    continue
                elif data[0] == '*':
                    # 后缀
                    key = FileIgnoreUtil.SUFFIX
                    data = data[1:]
                elif data[-1] == '*':
                    # 前缀
                    key = FileIgnoreUtil.PREFIX
                    data = data[:-1]
                elif data[-1] == '/':
                    # 文件夹
                    key = FileIgnoreUtil.FOLDER
                else:
                    # 文件
                    key = FileIgnoreUtil.FILE

                data = os.path.normpath(data)
                if key == FileIgnoreUtil.FOLDER:
                    data += '/'
                _ignore_dict[key].append(data)

        self.ignore_dict = dict()
        self.ignore_dict[FileIgnoreUtil.FILE] = set(_ignore_dict[FileIgnoreUtil.FILE])
        self.ignore_dict[FileIgnoreUtil.FOLDER] = tuple(set(_ignore_dict[FileIgnoreUtil.FOLDER]))
        self.ignore_dict[FileIgnoreUtil.PREFIX] = tuple(set(_ignore_dict[FileIgnoreUtil.PREFIX]))
        self.ignore_dict[FileIgnoreUtil.SUFFIX] = tuple(set(_ignore_dict[FileIgnoreUtil.SUFFIX]))

    def __contains__(self, item):

        if not self.ignore_dict:
            return False

        item = os.path.normpath(item)

        if item.startswith(self.ignore_dict[FileIgnoreUtil.FOLDER]):
            return True
        if item in self.ignore_dict[FileIgnoreUtil.FILE]:
            return True

        basename = os.path.basename(item)
        if basename.startswith(self.ignore_dict[FileIgnoreUtil.PREFIX]):
            return True
        if basename.endswith(self.ignore_dict[FileIgnoreUtil.SUFFIX]):
            return True
        return False
