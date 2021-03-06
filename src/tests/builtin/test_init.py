from unittest import TestCase
import os

import test_utils
from src.builtin.init import init

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'


class TestInit(TestCase):
    def test_init(self):
        test_utils.clean_arena()
        working_tree_dir = test_utils.get_arena_dir()
        os.path.curdir = working_tree_dir
        init()

        repo_dir = os.path.join(working_tree_dir, '.git/')
        branches_dir = os.path.join(repo_dir, 'branches')
        objects_dir = os.path.join(repo_dir, 'objects')
        refs_dir = os.path.join(repo_dir, 'refs')
        refs_heads_dir = os.path.join(refs_dir, 'heads')

        head_file = os.path.join(repo_dir, 'HEAD')

        self.assertTrue(os.path.exists(repo_dir), 'missing .git/ directory')
        self.assertTrue(os.path.exists(branches_dir), 'missing branches/ directory')
        self.assertTrue(os.path.exists(objects_dir), 'missing objects/ directory')
        self.assertTrue(os.path.exists(refs_dir), 'missing refs/ directory')
        self.assertTrue(os.path.exists(refs_heads_dir), 'missing refs/heads/ directory')

        self.assertTrue(os.path.exists(head_file), 'missing HEAD file')
