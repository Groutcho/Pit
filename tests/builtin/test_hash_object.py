from unittest import TestCase
from src.builtin import objects, init
from tests import test_utils
from src.builtin.objects import TreeEntry, Tree
import os.path
from binascii import hexlify

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'


class TestHashObject(TestCase):
    def test_hash_object_hash(self):
        ctx = test_utils.get_arena_context()
        file_to_hash = test_utils.create_arena_file('hello world\n', 'HELLO.txt')
        sha_1 = objects.hash_file(ctx, file_to_hash)

        self.assertEqual(b'3b18e512dba79e4c8300dd08aeb37f8e728b8dad', hexlify(sha_1), 'incorrect SHA-1 sum')

    def test_hash_object_write(self):
        test_utils.clean_arena()
        init.init(test_utils.get_arena_dir())

        ctx = test_utils.get_arena_context()
        file_to_hash = test_utils.create_arena_file('hello world\n', 'HELLO.txt')
        hexdigest = hexlify(objects.hash_file(ctx, file_to_hash, write_on_disk=True))
        hexdigest = hexdigest.decode()

        expected_dir = os.path.join(ctx.objects_dir, hexdigest[:2])
        expected_filename = os.path.join(expected_dir, hexdigest[2:])

        self.assertTrue(os.path.exists(expected_filename), 'the hashed object should be written on disk')

    def test_hash_tree(self):
        expected_sha1 = 'e4949fed0d9b455c75cc2e176bffd1ad3d5732d1'

        tree = Tree()
        tree.add_entry(TreeEntry('blob', 'AAAA', 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'))
        tree.add_entry(TreeEntry('blob', 'CCCC', 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'))
        tree.add_entry(TreeEntry('tree', 'subdir', '357c3fb20114a84e1ab0fd064f1d5e778ec111ef'))

        actual_sha1 = objects.hash_tree(None, tree)

        self.assertEqual(expected_sha1, actual_sha1, 'SHA-1 of tree object is incorrect')
