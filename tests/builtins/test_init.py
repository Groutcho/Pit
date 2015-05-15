from unittest import TestCase
import os
from tests import test_utils
from src.builtins.pit_init import init

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

class TestInit(TestCase):
  def test_init(self):
      test_utils.clean_arena()
      worktree_dir = test_utils.get_arena_dir()
      init(worktree_dir)
      repo_dir = os.path.join(worktree_dir, '.git/')
      self.assertTrue(os.path.exists(repo_dir), 'missing .git/ directory')
