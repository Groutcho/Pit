"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

handles hashing, writing and manipulating git objects
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from hashlib import sha1
import os
from binascii import hexlify, unhexlify

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


def hash_tree(ctx, tree, write_on_disk=False):
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
        write_sha1_object(ctx, hexdigest, header + content)

    return hexdigest


def hash_file(ctx, filename, write_on_disk=False):
    """appends the blob header to the file content
    and hashes the result

    see: http://www.git-scm.com/book/en/v2/Git-Internals-Git-Objects#Object-Storage

    """
    content = open(os.path.join(ctx.working_dir, filename), 'r').read().encode()
    size = len(content)

    header = ('blob %i\x00' % size).encode()

    sha1_object = sha1()
    sha1_object.update(header)
    sha1_object.update(content)

    hexdigest = sha1_object.hexdigest()
    digest = sha1_object.digest()

    if write_on_disk:
        write_sha1_object(ctx, hexdigest, header + content)

    return digest


def write_sha1_object(ctx, hexdigest, data):
    hash_prefix = hexdigest[:2]
    object_prefix_dir = os.path.join(ctx.objects_dir, hash_prefix)
    hash_filename = os.path.join(object_prefix_dir, hexdigest[2:])

    if not os.path.exists(object_prefix_dir):
        os.mkdir(object_prefix_dir)

    if not os.path.exists(hash_filename):
        fd = open(hash_filename, 'wb')
        fd.write(data)
