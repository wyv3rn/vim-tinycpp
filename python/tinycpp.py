from __future__ import print_function
import vim
import os
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def insert_include_guard():
    buf = vim.current.buffer
    filename = os.path.basename(buf.name)
    basename, ext = os.path.splitext(filename)
    guard = '{}_{}'.format(basename.upper(), ext.strip('.').upper())
    row, _ = vim.current.window.cursor
    new_lines = ['#ifndef {}'.format(guard), '#define {}'.format(guard), '', '#endif // {}'.format(guard)]
    buf.append(new_lines, row)

