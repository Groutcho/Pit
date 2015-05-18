from unittest import TestCase
from src.builtin import tree
from tests import test_utils
from src.builtin import index

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'


class TestWriteTree(TestCase):
    def test_write_tree(self):
        ctx = test_utils.setup_repo()
        fileA = test_utils.create_arena_file('', 'AAAA')
        fileB = test_utils.create_arena_file('', 'BBBB')
        index.update_index(ctx, [fileA, fileB])

        actual_sha1 = tree.write_tree(ctx)
        expected_sha1 = 'a43fd05ad4ffe1de9a2b4225b4715fedc79a8288'
        self.assertEqual(expected_sha1, actual_sha1)

    def test_commit_tree(self):
        ctx = test_utils.setup_repo()
        fileA = test_utils.create_arena_file('', 'AAAA')
        fileB = test_utils.create_arena_file('', 'BBBB')
        index.update_index(ctx, [fileA, fileB])
        sha_1 = tree.commit_tree(ctx,
                                 author_date='1431980072 +0200',
                                 author_email='<j.placeholder@example.org>',
                                 author_name='John Placeholder',
                                 description='this is the description')

        print(sha_1)
