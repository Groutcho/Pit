__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

import os
import shutil

ARENA_PATH = None


def get_file_dir(file):
    if file is None:
        raise TypeError
    return os.path.dirname(os.path.realpath(file))


def get_tests_dir():
    return os.path.dirname(os.path.realpath(__file__))


def get_arena_dir():
    global ARENA_PATH
    if ARENA_PATH is None:
        ARENA_PATH = os.path.join(get_tests_dir(), 'arena')
    return ARENA_PATH


def clean_arena():
    """must be called before each test that uses
    the arena"""
    folder = get_arena_dir()
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def create_arena_file(content, filename):
    """create a file in the arena. the filename must be
    relative."""
    full_path = os.path.join(ARENA_PATH, filename)
    fd = open(full_path, 'w')
    fd.write(content)
    fd.close()

    return full_path
