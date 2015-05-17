"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

handles writing and manipulating git trees
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from src.builtins.index import get_trees
from src.builtins.objects import hash_tree

def write_tree(ctx):
    """
    write the index trees and return the SHA-1 of the root tree

    """
    trees = get_trees(ctx)
    root = trees.pop('root')
    sha_1 = hash_tree(ctx, root, write_on_disk=True)

    for tree in trees:
        hash_tree(ctx, tree, write_on_disk=True)

    return sha_1
