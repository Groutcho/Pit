__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

from os import path

class PitContext():
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.repo_dir = path.join(working_dir, '.git/')
        self.objects_dir = path.join(self.repo_dir, 'objects/')
