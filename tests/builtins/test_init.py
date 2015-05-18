from unittest import TestCase
import os
from tests import test_utils
from src.builtins.init import init

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'


class TestInit(TestCase):
    def test_init(self):
        test_utils.clean_arena()
        working_tree_dir = test_utils.get_arena_dir()
        init(working_tree_dir)

        repo_dir = os.path.join(working_tree_dir, '.git/')
        branches_dir = os.path.join(repo_dir, 'branches')
        objects_dir = os.path.join(repo_dir, 'objects')
        refs_dir = os.path.join(repo_dir, 'refs')

        HEAD_file = os.path.join(repo_dir, 'HEAD')

        self.assertTrue(os.path.exists(repo_dir), 'missing .git/ directory')
        self.assertTrue(os.path.exists(branches_dir), 'missing branches/ directory')
        self.assertTrue(os.path.exists(objects_dir), 'missing objects/ directory')
        self.assertTrue(os.path.exists(refs_dir), 'missing refs/ directory')

        self.assertTrue(os.path.exists(HEAD_file), 'missing HEAD file')
