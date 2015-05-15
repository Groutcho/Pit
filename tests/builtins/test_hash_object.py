from unittest import TestCase
from src.builtins import objects, pit_init
from tests import test_utils
import os.path

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'


class TestHashObject(TestCase):
    def test_hash_object_hash(self):
        ctx = test_utils.get_arena_context()
        file_to_hash = test_utils.create_arena_file('hello world\n', 'HELLO.txt')
        hexdigest = objects.hash_object(ctx, file_to_hash)

        self.assertEqual('3b18e512dba79e4c8300dd08aeb37f8e728b8dad', hexdigest)

    def test_hash_object_write(self):
        test_utils.clean_arena()
        pit_init.init(test_utils.get_arena_dir())

        ctx = test_utils.get_arena_context()
        file_to_hash = test_utils.create_arena_file('hello world\n', 'HELLO.txt')
        hexdigest = objects.hash_object(ctx, file_to_hash, write_on_disk=True)

        expected_dir = os.path.join(ctx.objects_dir, hexdigest[:2])
        expected_filename = os.path.join(expected_dir, hexdigest[2:])

        self.assertTrue(os.path.exists(expected_filename), 'the hashed object should be written on disk')
