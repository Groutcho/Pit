# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

context.py: give the repository context (paths to working tree, .git/ ...)
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

import os

class PitContext:
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.repo_dir = os.path.join(working_dir, '.git/')
        self.objects_dir = os.path.join(self.repo_dir, 'objects/')
        self.index = os.path.join(self.repo_dir, 'index')
        self.head = os.path.join(self.repo_dir, 'HEAD')

    def get_current_branch_file(self):
        fd = open(self.head, 'r')
        content = fd.read()
        branch_file = content.rsplit('ref: ')[1]
        return os.path.join(self.repo_dir, branch_file)


def get_context():
    curdir = os.path.curdir
    while curdir != '/':
        if os.path.exists(os.path.join(curdir, '.git')):
            return PitContext(curdir)
        else:
            curdir = os.path.split(curdir)[0]
    else:
        print('fatal: Not a git repository')
