# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

handles index (aka 'staging area') creation and manipulation
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from builtin.objects import hash_file, Tree, TreeEntry
from hashlib import sha1
from binascii import hexlify, unhexlify
import context
import os
import struct


def update_index(objects):
    """rewrite the index file with the given objects"""

    ctx = context.get_context()

    # index file header ('dir cache')
    data = b'DIRC'

    # version number (for now, 2)
    # on 4 bytes
    data += b'\x00\x00\x00\x02'

    # number of entries on 4 bytes
    # for now, limit it to 255 entries
    data += ('\x00\x00\x00' + chr(len(objects))).encode()

    # write the actual entries
    for o in objects:
        stat = os.stat(o)

        data += struct.pack('>f', stat.st_ctime)
        data += struct.pack('>f', stat.st_ctime_ns)
        data += struct.pack('>f', stat.st_mtime)
        data += struct.pack('>f', stat.st_mtime_ns)
        data += stat.st_dev.to_bytes(4, byteorder='big')
        data += stat.st_ino.to_bytes(4, byteorder='big')
        # even though the Git specification allows symlinks and gitlinks,
        # as well as mode 755, consider all entries as files with permission 644
        data += b'\x00\x00\x81\xa4'
        data += stat.st_uid.to_bytes(4, byteorder='big')
        data += stat.st_gid.to_bytes(4, byteorder='big')
        data += stat.st_size.to_bytes(4, byteorder='big')

        # 20-bytes SHA-1 for the current object
        sha_1 = hash_file(o, write_on_disk=True)
        data += unhexlify(sha_1)

        # filename size without padding
        data += len(o).to_bytes(2, byteorder='big')

        # the filename
        data += o.encode()

        # pad the entry with NULs to ensure that it's a multiple of 8 (while being NUL terminated)
        entry_size = len(o) + 62
        data += ((entry_size - (entry_size % 8) + 8) - entry_size) * b'\x00'

    # compute the SHA-1 of the data so far and append it as
    # the last value in the index file
    index_sha = sha1()
    index_sha.update(data)
    index_sha_value = index_sha.digest()
    data += index_sha_value

    fd = open(ctx.index, 'wb')
    fd.write(data)
    fd.close()


def get_entries(pathnames_only=False):
    ctx = context.get_context()

    if not os.path.exists(ctx.index):
        return []

    fd = open(ctx.index, 'rb')
    content = fd.read()
    number_of_entries = int.from_bytes(content[8:12], byteorder='big')
    fd.close()
    pos = 12

    entries = []

    while number_of_entries > 0:
        # skip 40 non implemented bytes
        pos += 40

        # read the SHA-1 of the current entry
        sha_1 = content[pos:pos + 20]

        # skip the SHA-1
        pos += 20

        # skip 2 non implemented bytes
        pos += 2

        offset = 0
        while content[pos + offset] is not 0:
            offset += 1

        pathname = (content[pos:pos + offset])
        pos += offset

        while content[pos] is 0:
            pos += 1

        number_of_entries -= 1
        if pathnames_only:
            entries.append(pathname.decode())
        else:
            entries.append(('blob', pathname, hexlify(sha_1)))

    return entries


def get_trees():
    entries = get_entries()

    trees = {'root': Tree()}
    for entry in entries:
        pathname = entry[1].decode()
        sha_1 = entry[2]
        if '/' in pathname:
            elements = pathname.split('/')
            trees['root'].add_entry(TreeEntry('tree', elements[0]))
            for i in range(len(elements) - 1):
                name = elements[i]
                pointed_object = elements[i + 1]
                object_type = 'blob' if i + 1 is (len(elements) - 1) else 'tree'

                if trees.get(name) is None:
                    trees[name] = Tree()
                trees[name].add_entry(TreeEntry(object_type, pointed_object))
        else:
            # no forward slash, it's a file in the root directory
            trees['root'].add_entry(TreeEntry('blob', pathname, sha_1))

    return trees
