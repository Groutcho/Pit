__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

""" pit_init.py - initialize a Git repository """

import os.path

def init(worktree_dir):
    os.mkdir(os.path.join(worktree_dir, '.git/'))
    pass
