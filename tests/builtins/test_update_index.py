# coding: utf-8

from unittest import TestCase
from tests import test_utils
from src.builtins import index
from binascii import hexlify

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

HELLO_SHA1 = b'ce013625030ba8dba906f756967f9e9ca394464a'


class TestIndex(TestCase):
    def test_index_header_is_dirc(self):
        ctx = test_utils.setup_repo()
        hellofile = test_utils.create_arena_file('hello\n', 'HELLO.txt')
        index.update_index(ctx, [hellofile])
        fd = open(ctx.index, 'rb')
        index_content = fd.read()
        fd.close()

        self.assertEqual('DIRC'.encode(), index_content[:4], 'incorrect index header (must be DIRC)')
        self.assertEqual(HELLO_SHA1, hexlify(index_content[52:][:20]), 'incorrect SHA-1')
        self.assertEqual('HELLO.txt\x00\x00\x00\x00\x00\x00\x00', index_content[74:][:16].decode(), 'incorrect padding'
                                                                                           ' of filename')

    def test_get_entries(self):
        ctx = test_utils.setup_repo()
        hellofile = test_utils.create_arena_file('hello\n', 'HELLO.txt')
        worldfile = test_utils.create_arena_file('hello\n', 'WORLD.txt')
        index.update_index(ctx, [hellofile, worldfile])
        entries = index.get_entries(ctx)
        expected = [('blob', b'HELLO.txt', HELLO_SHA1), ('blob', b'WORLD.txt', HELLO_SHA1)]
        self.assertEqual(entries, expected, 'extracted entries incorrect')
