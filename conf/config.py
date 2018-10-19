#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/9
# @Author  : aimkiray

import configparser
import os
import file


class Config(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        # self.raw_conf_path = os.path.join(os.path.dirname(os.path.abspath('.')), r'raw\config.ini')
        # raw_conf_dir = r'raw\config.ini'
        # self.raw_conf_path = os.path.join(raw_conf_dir, 'config.ini')
        self.raw_conf_path = file.find_path(r'raw\config.ini')
        # conf_dir = r'conf'
        # self.conf_path = os.path.join(conf_dir, 'config.ini')
        self.conf_path = r'config.ini'
        if not os.path.exists(self.conf_path):
            with open(self.raw_conf_path, 'r') as f:
                self.raw_config = f.read()
            with open(self.conf_path, 'w') as f:
                f.write(self.raw_config)
        self.config.read(self.conf_path, encoding='utf-8-sig')  # Read the configuration file

        # See custom tools.gen_config.py
        self.conf = {
            'pac_file_path': '', 'pac_server_port': '', 'address': ''
        }

    def get_config(self):
        """
        Read configuration file parameters and assign them to global parameters
        See custom tools.gen_config.py
        """
        self.conf['pac_file_path'] = self.config.get('proxy', 'pac_file_path')
        self.conf['pac_server_port'] = self.config.get('proxy', 'pac_server_port')
        self.conf['address'] = self.config.get('proxy', 'address')

        return self.conf

    def set_config(self, modified):
        self.config.set('proxy', 'pac_file_path', modified.pac)
        self.config.set('proxy', 'pac_server_port', modified.pac_port)
        self.config.set('proxy', 'address', modified.address)

        with open(self.conf_path, 'w') as f:
            self.config.write(f)


if __name__ == '__main__':
    Config()
