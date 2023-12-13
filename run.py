#!/usr/bin/env python

import argparse
import os
import subprocess
from typing import List
import unittest

def arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run server, test'
    )

    subparsers = parser.add_subparsers(dest='func')

    subparsers.add_parser('test')
    subparsers.add_parser('server')

    return parser


def run_server() -> None:
    subprocess.call(['python3', 'app.py'])


def run_tests() -> None:
    verbosity = 1
    test_suite = unittest.TestLoader().discover('test', pattern='*_test.py')
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)


def main(args=None) -> None:
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    parser = arg_parser()
    args = parser.parse_args(args)

    actions = {
        'server': lambda: run_server(),
        'test': lambda: run_tests(),
    }

    actions.get(args.func, parser.print_help)()


if __name__ == "__main__":
    main()