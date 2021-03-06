# coding: utf-8

from unittest import TestCase
from binascii import hexlify

import test_utils
from src.builtin import index

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

HELLO_SHA1 = b'ce013625030ba8dba906f756967f9e9ca394464a'


class TestIndex(TestCase):
    def test_index_header_is_dirc(self):
        ctx = test_utils.setup_repo()
        hellofile = test_utils.create_arena_file('hello\n', 'HELLO.txt')
        index.update_index([hellofile])
        fd = open(ctx.index, 'rb')
        index_content = fd.read()
        fd.close()

        self.assertEqual('DIRC'.encode(), index_content[:4], 'incorrect index header (must be DIRC)')
        self.assertEqual(HELLO_SHA1, hexlify(index_content[52:][:20]), 'incorrect SHA-1')
        self.assertEqual('HELLO.txt\x00', index_content[74:][:10].decode(), 'incorrect padding'
                                                                                           ' of filename')

    def test_get_entries(self):
        test_utils.setup_repo()
        hellofile = test_utils.create_arena_file('hello\n', 'HELLO.txt')
        worldfile = test_utils.create_arena_file('hello\n', 'WORLD.txt')
        index.update_index([hellofile, worldfile])
        entries = index.get_entries()

        self.assertEqual(entries[0].sha_1, HELLO_SHA1)
        self.assertEqual(entries[1].sha_1, HELLO_SHA1)
        self.assertEqual(entries[0].pathname, 'HELLO.txt')
        self.assertEqual(entries[1].pathname, 'WORLD.txt')

    def test_extract_trees(self):
        test_utils.setup_repo()
        hellofile = test_utils.create_arena_file('hello\n', 'HELLO.txt')
        worldfile = test_utils.create_arena_file('hello\n', 'WORLD.txt')
        nested_file = test_utils.create_arena_file('hello\n', 'subdir/NESTED.txt')
        index.update_index([hellofile, worldfile, nested_file])
        trees = index.get_trees()

        self.assertTrue(trees['root'].contains_entry('HELLO.txt'))
        self.assertTrue(trees['root'].contains_entry('WORLD.txt'))
        self.assertTrue(trees['root'].contains_entry('subdir'))

        self.assertTrue(trees['subdir'].contains_entry('NESTED.txt'))
