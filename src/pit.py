# coding: utf-8

"""
Pit - Git in python

Copyright (C) 2015  Sébastien Guimmara

pit.py: call commands according to user input
"""

__author__ = 'Sébastien Guimmara <sebastien.guimmara@gmail.com>'

import sys
import getopt
import builtin.init


command_map = {'init': builtin.init.init}


def usage():
    print('usage: pit <command> [<args>]')


def version():
    print('pit version 0.0.1')


def main(argv):
    if len(argv) == 1:
        usage()

    try:
        opts, args = getopt.getopt(argv, 'vh', ['help', 'version'])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for arg in args:
        if arg in command_map.keys():
            command_map[arg](argv)

    for o, a in opts:
        if o in ['-v', '--version']:
            version()
            sys.exit(0)
        else:
            assert False, 'unrecognized pit command: ' + o


if __name__ == '__main__':
    main(sys.argv)
