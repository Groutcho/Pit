"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

handles hashing, writing and manipulating git objects
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from hashlib import sha1
import os

class TreeEntry:
    def __init__(self, etype='blob', name=None, sha_1=None):
        self.type = etype
        self.sha_1 = sha_1
        self.name = name

    def __repr__(self):
        return '%s %s %s' % (self.type, self.name, self.sha_1)


class Tree:
    def __init__(self):
        self.entries = []
        self.sha1 = None

    def add_entry(self, entry):
        if not self.contains_entry(entry.name):
            self.entries.append(entry)
            self.compute_sha1()

    def contains_entry(self, name):
        for entry in self.entries:
            if entry.name is name:
                return True
        return False

    def compute_sha1(self):
        pass


def hash_tree(pit_ctx, tree, write_on_disk=False)

    size = 0
    content = ''
    for entry in tree:
        if entry

    header = ('tree %i\x00' % size).encode()
    sha1_object = sha1()


def hash_file(pit_context, filename, write_on_disk=False):
    """appends the blob header to the file content
    and hashes the result

    see: http://www.git-scm.com/book/en/v2/Git-Internals-Git-Objects#Object-Storage

    """
    content = open(os.path.join(pit_context.working_dir, filename), 'r').read().encode()
    size = len(content)

    header = ('%s %i\x00' % (object_type, size)).encode()

    sha1_object = sha1()
    sha1_object.update(header)
    sha1_object.update(content)

    hexdigest = sha1_object.hexdigest()

    if write_on_disk:
        hash_prefix = hexdigest[:2]
        object_prefix_dir = os.path.join(pit_context.objects_dir, hash_prefix)
        hash_filename = os.path.join(object_prefix_dir, hexdigest[2:])

        if not os.path.exists(object_prefix_dir):
            os.mkdir(object_prefix_dir)

        if not os.path.exists(hash_filename):
            fd = open(hash_filename, 'wb')
            fd.write(header + content)

    return hexdigest
