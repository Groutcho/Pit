"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

initialize an empty Git repository
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

import os.path

def init(working_tree_dir):

    repo_dir = os.path.join(working_tree_dir, '.git/')
    branches_dir = os.path.join(repo_dir, 'branches')
    objects_dir = os.path.join(repo_dir, 'objects')
    refs_dir = os.path.join(repo_dir, 'refs')

    HEAD_file = os.path.join(repo_dir, 'HEAD')

    os.mkdir(repo_dir)
    os.mkdir(branches_dir)
    os.mkdir(objects_dir)
    os.mkdir(refs_dir)

    os.mknod(HEAD_file, mode=666)


