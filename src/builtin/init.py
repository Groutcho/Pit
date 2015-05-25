# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

initialize an empty Git repository
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

import os.path
import sys

def init(argv=None):
    working_tree_dir = os.path.curdir
    repo_dir = os.path.join(working_tree_dir, '.git/')

    if os.path.exists(repo_dir):
        print('abort: .git/ directory already exists')
        sys.exit(2)

    branches_dir = os.path.join(repo_dir, 'branches')
    objects_dir = os.path.join(repo_dir, 'objects')
    refs_dir = os.path.join(repo_dir, 'refs')
    refs_heads_dir = os.path.join(refs_dir, 'heads')

    head_file = os.path.join(repo_dir, 'HEAD')

    os.mkdir(repo_dir)
    os.mkdir(branches_dir)
    os.mkdir(objects_dir)
    os.mkdir(refs_dir)
    os.mkdir(refs_heads_dir)

    os.mknod(head_file, 0o666)
    fd = open(head_file, 'w')
    fd.write('ref: refs/heads/master')
    fd.close()

    print("initialized empty git repository in .git/")
