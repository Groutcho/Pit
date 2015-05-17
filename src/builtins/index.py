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
