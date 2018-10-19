#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 3/14/2018
# @Author : aimkiray
# @Email  : root@meowwoo.com

import re

# read config.ini
with open(r'..\raw\config.ini', 'r') as config_file:
    raw_fields = config_file.read()


class GenConfig(object):

    def __init__(self, fields):
        super(GenConfig, self).__init__()
        self.fields = fields

    def gen_empty(self):
        name_list = re.findall(r'(?<=\n).*(?= =)', self.fields)
        complete = ""
        for index in range(len(name_list)):
            complete = complete + '\'' + name_list[index] + '\': \'\' ,'
        print(complete[:-2])

    def gen_equals(self):
        group = re.split(r'(?<=\n)\n(?=\[)', self.fields)
        for part in group:
            title = re.findall(r'(?<=\[).*(?=\])', part)
            name_list = re.findall(r'(?<=\n).*(?= =)', part)
            complete = ""
            for index in range(len(name_list)):
                complete = complete + 'self.conf[\'' + name_list[index] + '\'] = self.config.get(\'' + title[
                    0] + '\', \'' + name_list[index] + '\')\n'
            print(complete)

    def gen_set(self):
        group = re.split(r'(?<=\n)\n(?=\[)', self.fields)
        for part in group:
            title = re.findall(r'(?<=\[).*(?=\])', part)
            name_list = re.findall(r'(?<=\n).*(?= =)', part)
            # value_list = re.findall(r'(?<== ).*(?=\n)', part)
            complete = ""
            for index in range(len(name_list)):
                complete = complete + 'self.config.set(\'' + title[
                    0] + '\', \'' + name_list[index] + '\', modified.' + name_list[index] + ')\n'
            print(complete)


if __name__ == '__main__':
    export = GenConfig(raw_fields)
    export.gen_empty()
    export.gen_equals()
    export.gen_set()
