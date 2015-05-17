"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

handles index (aka 'staging area') creation and manipulation
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from src.builtins.objects import hash_object
from hashlib import sha1
from os import path


def update_index(pit_ctx, objects):
    """rewrite the index file with the given objects"""

    # index file header ('dir cache')
    data = 'DIRC'

    # version number (for now, 2)
    # on 4 bytes
    data += '\x00\x00\x00\x02'

    # number of entries on 4 bytes
    # for now, limit it to 255 entries
    data += '\x00\x00\x00'
    data += chr(len(objects))

    # write the actual entries
    for o in objects:
        # 40 bytes padding (to be implemented later)
        # those bytes store metadata about permissions, size,
        # time since modification, bit flags...
        data += 40 * '\x30'

        # 20 bytes SHA-1 for the current object
        object_sha1 = hash_object(pit_ctx, o, 'blob', write_on_disk=True)
        data += object_sha1

        # 16 bits flags for future implementation
        data += '\x00\x00'

        # the filename
        data += o

        # the filename padded with NUL to a multiple of 8
        data += (8 - len(o) % 8) * '\x00'

    # compute the SHA-1 of the data so far and append it as
    # the last value in the index file
    index_sha = sha1()
    index_sha.update(data.encode())
    index_sha_value = index_sha.hexdigest()
    data += index_sha_value

    fd = open(pit_ctx.index, 'wb')
    fd.write(data.encode())
    fd.close()


def extract_entries_from_index(pit_ctx):
    fd = open(pit_ctx.index, 'r')
    content = fd.read()
    number_of_entries = int.from_bytes(content[8:12].encode(), byteorder='big')
    fd.close()
    pos = 12

    entries = []

    while number_of_entries > 0:
        # skip 40 non implemented bytes
        pos += 40

        # read the SHA-1 of the current entry
        sha1 = content[pos:pos+40]

        # skip the SHA-1
        pos += 40

        # skip 2 non implemented bytes
        pos += 2

        offset = 0
        while content[pos+offset] is not '\x00':
            offset += 1

        pathname = content[pos:pos+offset]
        pos += offset

        while content[pos] is '\x00':
            pos += 1

        number_of_entries -= 1
        entries.append((pathname, sha1))

    return entries
