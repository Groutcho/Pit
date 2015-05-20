from unittest import TestCase
import tests.test_utils
from src.builtin import index, add

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'


class TestAdd(TestCase):
    def test_add(self):
        tests.test_utils.setup_repo()
        file_a = tests.test_utils.create_arena_file('', 'AAAA')
        file_b = tests.test_utils.create_arena_file('', 'BBBB')
        file_c = tests.test_utils.create_arena_file('', 'CCCC')
        index.update_index([file_a, file_b, file_c])
        file_d = tests.test_utils.create_arena_file('', 'DDDD')
        add.add(['pit', 'add', file_d])
        actual_entries = index.get_entries(pathnames_only=True)
        expected_entries = ['AAAA', 'BBBB', 'CCCC', 'DDDD']
        self.assertEqual(actual_entries, expected_entries)
