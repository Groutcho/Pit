__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from hashlib import sha1


def hash_object(filename):
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
    return sha1_object.hexdigest()
