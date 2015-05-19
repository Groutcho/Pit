# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

handles writing and manipulating git trees
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from builtin.index import get_trees
from builtin.objects import hash_tree, hash_commit
import context

def write_tree():
    """
    write the index trees and return the SHA-1 of the root tree

    """
    ctx = context.get_context()
    trees = get_trees()
    root = trees.pop('root')
    sha_1 = hash_tree(root, write_on_disk=True)

    for tree in trees:
        hash_tree(tree, write_on_disk=True)

    return sha_1


def commit_tree(**kwargs):
    """
    take the tree contained in the index and
    write a commit objects whose layout is following:

    ====================================================================
    commit 358<NUL>tree d306b9e74803fe248c420d731274a02e80c6619e
    parent 6ceb2b9655a2c92c183c2bb7e8e2861f49edff0c
    author John Placeholder <j.placeholder@example.org> 1431980072 +0200
    committer John Placeholder <j.placeholder@example.org> 1431980072 +0200

    <commit description>
    ====================================================================
    """

    author_name = kwargs['author_name']
    author_email = kwargs['author_email']
    author_date = kwargs['author_date']

    committer_name = kwargs['committer_name'] if 'commiter_name' in kwargs.keys() else None
    committer_email = kwargs['committer_email'] if 'committer_email' in kwargs.keys() else None
    committer_date = kwargs['committer_date'] if 'committer_date' in kwargs.keys() else None

    description = kwargs['description']

    tree_sha_1 = write_tree()
    parent_commit = kwargs['parent_commit'] if 'parent_commit' in kwargs.keys() else None
    content = 'tree %s\n' % tree_sha_1
    if parent_commit is not None:
        content += 'parent %s\n' % parent_commit
    content += 'author {0:s} {1:s} {2:s}\n'.format(author_name, author_email, author_date)

    if committer_name is not None and committer_email is not None and committer_date is not None:
        content += 'committer {0:s} {1:s} {2:s}\n'.format(committer_name, committer_email, committer_date)

    content += '\n'
    content += description
    content += '\n'

    return hash_commit(content.encode(), write_on_disk=True)
