from unittest import TestCase
from tests import test_utils
from src.builtins import objects

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'


class TestHashObject(TestCase):
  def test_hash_object(self):
    file_to_hash = test_utils.create_arena_file('hello world\n', 'HELLO.txt')
    hexdigest = objects.hash_object(file_to_hash)

    self.assertEqual('3b18e512dba79e4c8300dd08aeb37f8e728b8dad', hexdigest)
