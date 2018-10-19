#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10
# @Author  : aimkiray


import os


def find_path(file):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(project_dir, file)
