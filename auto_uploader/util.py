#!/usr/bin/env python3
# coding=utf-8
#
# Copyright 2018, Mice Pápai
# Created: 2018.01.22. 13:00
#
import os
import sys
from os.path import isfile


def print_progress(current,
                   total,
                   prefix: str = '',
                   suffix: str = '',
                   decimals: int = 1,
                   bar_length: int = 50,
                   fill_char: str = '█'):
    """Displays a progress bar"""

    current = min(current, total)

    percent = 100 * (current / float(total))
    filled_length = int(round(bar_length * current / float(total)))

    bar = fill_char * filled_length + '-' * (bar_length - filled_length)
    output = f'\r{prefix} |{bar}| {percent:.{decimals}f}% {suffix}\r'

    sys.stdout.write(output)
    sys.stdout.flush()

    if current == total:
        print()


jn = os.path.join


def get_files(folder):
    return sorted([jn(folder, f) for f in os.listdir(folder)
                   if isfile(jn(folder, f))])
