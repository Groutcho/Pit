# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

handles hashing, writing and manipulating git objects
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from hashlib import sha1
import os
from binascii import unhexlify
import zlib
import context


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
            if entry.name == name:
                return True
        return False

    def compute_sha1(self):
        pass


def hash_tree(tree, write_on_disk=False):
    content = b''
    for entry in tree.entries:
        if entry.type is 'blob':
            # file permission followed by a space
            content += '100644 '.encode()
        elif entry.type is 'tree':
            content += '40000 '.encode()
        content += (entry.name + '\x00').encode()
        content += unhexlify(entry.sha_1)

    header = ('tree %i\x00' % len(content)).encode()
    sha1_object = sha1()
    sha1_object.update(header)
    sha1_object.update(content)

    hexdigest = sha1_object.hexdigest()

    if write_on_disk:
        write_sha1_object(hexdigest, header + content)

    return hexdigest


def hash_file(filename, write_on_disk=False):
    """
    appends the blob header to the file content and hashes the result

    see: http://www.git-scm.com/book/en/v2/Git-Internals-Git-Objects#Object-Storage

    """
    ctx = context.get_context()
    content = open(os.path.join(ctx.working_dir, filename), 'r').read().encode()
    size = len(content)

    header = ('blob %i\x00' % size).encode()

    sha1_object = sha1()
    sha1_object.update(header)
    sha1_object.update(content)

    hexdigest = sha1_object.hexdigest()

    if write_on_disk:
        write_sha1_object(hexdigest, header + content)

    return hexdigest


def write_sha1_object(hexdigest, data):
    ctx = context.get_context()
    hash_prefix = hexdigest[:2]
    object_prefix_dir = os.path.join(ctx.objects_dir, hash_prefix)
    hash_filename = os.path.join(object_prefix_dir, hexdigest[2:])

    if not os.path.exists(object_prefix_dir):
        os.mkdir(object_prefix_dir)

    if not os.path.exists(hash_filename):
        fd = open(hash_filename, 'wb')
        fd.write(zlib.compress(data))


def hash_commit(data, write_on_disk=False):
    ctx = context.get_context()
    header = ('commit {0:d}\x00'.format(len(data))).encode()
    sha1_object = sha1()
    sha1_object.update(header)
    sha1_object.update(data)

    hexdigest = sha1_object.hexdigest()

    if write_on_disk:
        write_sha1_object(hexdigest, header + data)

    return hexdigest
