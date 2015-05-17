from unittest import TestCase
from tests import test_utils
from src.builtins import index

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

HELLO_SHA1 = b'ce013625030ba8dba906f756967f9e9ca394464a'


class TestIndex(TestCase):
    def test_index_header_is_dirc(self):
        ctx = test_utils.setup_repo()
        hellofile = test_utils.create_arena_file('hello\n', 'HELLO.txt')
        index.update_index(ctx, [hellofile])
        index_content = open(ctx.index, 'rb').read()

        self.assertEqual('DIRC'.encode(), index_content[:4], 'incorrect index header (must be DIRC)')
        self.assertEqual(HELLO_SHA1, index_content[52:][:40], 'incorrect SHA-1')
        self.assertEqual('HELLO.txt\x00\x00\x00\x00\x00\x00\x00', index_content[94:][:16].decode(), 'incorrect padding'
                                                                                                    ' of filename')

    def test_extract_entries_from_index(self):
        ctx = test_utils.setup_repo()
        hellofile = test_utils.create_arena_file('hello\n', 'HELLO.txt')
        worldfile = test_utils.create_arena_file('hello\n', 'WORLD.txt')
        index.update_index(ctx, [hellofile, worldfile])
        entries = index.extract_entries_from_index(ctx)
        expected = [('HELLO.txt', HELLO_SHA1.decode('utf-8')), ('WORLD.txt', HELLO_SHA1.decode('utf-8'))]
        self.assertEqual(entries, expected, 'extracted entries incorrect')
