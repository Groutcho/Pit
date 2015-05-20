# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

handles index (aka 'staging area') creation and manipulation
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

import src.builtin.objects as objects
from hashlib import sha1
from binascii import hexlify, unhexlify
import context
import os
import struct


class IndexEntry:
    def __init__(self, pathname, sha_1, stat_info):
        self.pathname = pathname
        self.sha_1 = sha_1
        self.stat_info = stat_info

    def to_bytes(self):
        data = self.stat_info.to_bytes()
        data += unhexlify(self.sha_1)
        data += len(self.pathname).to_bytes(2, byteorder='big')
        data += self.pathname.encode()
        entry_size = len(data)
        data += ((entry_size - (entry_size % 8) + 8) - entry_size) * b'\x00'
        return data


class StatInfo:
    def __init__(self):
        self.ctime = 0
        self.ctime_ns = 0
        self.mtime = 0
        self.mtime_ns = 0
        self.dev = 0
        self.ino = 0
        self.mode = 0
        self.uid = 0
        self.gid = 0
        self.size = 0

    def to_bytes(self):
        data = b''
        data += struct.pack('>f', self.ctime)
        data += struct.pack('>f', self.ctime_ns)
        data += struct.pack('>f', self.mtime)
        data += struct.pack('>f', self.mtime_ns)
        data += self.dev.to_bytes(4, byteorder='big')
        data += self.ino.to_bytes(4, byteorder='big')
        # even though the Git specification allows symlinks and gitlinks,
        # as well as mode 755, consider all entries as files with permission 644
        data += b'\x00\x00\x81\xa4'
        data += self.uid.to_bytes(4, byteorder='big')
        data += self.gid.to_bytes(4, byteorder='big')
        data += self.size.to_bytes(4, byteorder='big')
        return data


def update_index(pathnames):
    """rewrite the index file with the given objects"""

    ctx = context.get_context()
    entries = get_entries()

    # compare the entries in index with what we want to add from the work tree
    # if the SHA-1s match, skip this entry: the file has not been modified
    for p in pathnames:
        add_entry = True
        for i in range(len(entries)):
            if entries[i].pathname == p and entries[i].sha_1 == objects.hash_file(p, write_on_disk=False):
                add_entry = False
        if add_entry:
            entries.append(create_entry(p))

    # index file header ('dir cache')
    data = b'DIRC'

    # version number (for now, 2)
    # on 4 bytes
    data += b'\x00\x00\x00\x02'

    # number of entries on 4 bytes
    # for now, limit it to 255 entries
    data += ('\x00\x00\x00' + chr(len(entries))).encode()

    # write the actual entries (sorted by bytes)
    for o in sorted(entries, key=lambda ent: bytes(ent.pathname, encoding='utf-8')):
        data += o.to_bytes()

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
        stat_info = extract_stat_info(content[pos:pos+40])
        pos += 40

        # read the SHA-1 of the current entry
        sha_1 = hexlify(content[pos:pos + 20])
        pos += 20

        # skip 2 non implemented bytes
        pathname_size = int.from_bytes(content[pos:pos+2], byteorder='big')
        pos += 2

        pathname = (content[pos:pos + pathname_size]).decode()
        pos += pathname_size

        current_entry = IndexEntry(pathname, sha_1, stat_info)

        while content[pos] is 0:
            pos += 1

        number_of_entries -= 1
        if pathnames_only:
            entries.append(pathname)
        else:
            entries.append(current_entry)

    return entries


def get_trees():
    entries = get_entries()

    trees = {'root': objects.Tree()}
    for entry in entries:
        pathname = entry.pathname
        sha_1 = entry.sha_1
        if '/' in pathname:
            elements = pathname.split('/')
            trees['root'].add_entry(objects.TreeEntry('tree', elements[0]))
            for i in range(len(elements) - 1):
                name = elements[i]
                pointed_object = elements[i + 1]
                object_type = 'blob' if i + 1 is (len(elements) - 1) else 'tree'

                if trees.get(name) is None:
                    trees[name] = objects.Tree()
                trees[name].add_entry(objects.TreeEntry(object_type, pointed_object))
        else:
            # no forward slash, it's a file in the root directory
            trees['root'].add_entry(objects.TreeEntry('blob', pathname, sha_1))

    return trees


def extract_stat_info(buffer):
    assert len(buffer) == 40
    result = StatInfo()
    result.ctime = struct.unpack('>f', buffer[0:4])[0]
    result.ctime_ns = struct.unpack('>f', buffer[4:8])[0]
    result.mtime = struct.unpack('>f', buffer[8:12])[0]
    result.mtime_ns = struct.unpack('>f', buffer[12:16])[0]
    result.dev = struct.unpack('>i', buffer[16:20])[0]
    result.ino = struct.unpack('>i', buffer[20:24])[0]
    result.mode = struct.unpack('>i', buffer[24:28])[0]
    result.uid = struct.unpack('>i', buffer[28:32])[0]
    result.gid = struct.unpack('>i', buffer[32:36])[0]
    result.size = struct.unpack('>i', buffer[36:40])[0]

    return result


def create_entry(pathname):
    assert not os.path.isabs(pathname)
    ctx = context.get_context()

    stat = os.stat(os.path.join(ctx.working_dir, pathname))
    stat_info = StatInfo()
    stat_info.ctime = stat.st_ctime
    stat_info.ctime_ns = stat.st_ctime_ns
    stat_info.mtime = stat.st_mtime
    stat_info.mtime_ns = stat.st_mtime_ns
    stat_info.dev = stat.st_dev
    stat_info.ino = stat.st_ino
    stat_info.mode = 33188
    stat_info.uid = stat.st_uid
    stat_info.gid = stat.st_gid
    stat_info.size = stat.st_size

    sha_1 = objects.hash_file(pathname, write_on_disk=True)
    return IndexEntry(pathname, sha_1, stat_info)
