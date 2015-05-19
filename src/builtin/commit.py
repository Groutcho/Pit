# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

commit.py: builtin command to commit tree
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

import builtin.tree as tree
import getopt


def commit(argv):
    message = ''
    opts, args = getopt.getopt(argv[2:], 'm:')
    for o, a in opts:
        if o == '-m':
            message = a
    tree.commit_tree(author_date='1431980072 +0200',
                     author_email='<j.placeholder@example.org>',
                     author_name='John Placeholder',
                     description=message)
