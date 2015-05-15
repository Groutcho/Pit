__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from hashlib import sha1
import os


def hash_object(pit_context, filename, write_on_disk=False):
    """appends the blob header to the file content
    and hashes the result

    see: http://www.git-scm.com/book/en/v2/Git-Internals-Git-Objects#Object-Storage

    """
    content = open(filename, 'r').read().encode()
    size = len(content)

    header = 'blob {0}\x00'.format(size).encode()

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
