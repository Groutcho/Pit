# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

add.py: add files to index
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

import context
import os
from builtin import index
import sys

def add(argv):
    """
    'pit add' expects a list of files to add and optional arguments
    """
    ctx = context.get_context()
    files_to_add = argv[2:]
    entries = index.get_entries(pathnames_only=True)
    for f in files_to_add:
        if not os.path.exists(os.path.join(ctx.working_dir, f)):
            print('fatal: pathspec "%s" did not match any files' % f)
            sys.exit(2)

    index.update_index(entries + files_to_add)
