from __future__ import print_function
import vim
import os
import sys
import re

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_current_context():
    buf, (row, col) = vim.current.buffer, vim.current.window.cursor
    return buf, row, col

# check if the current line in inside a class/struct definition and return its name (None otherwise)
def get_class_name():
    buf, row, _ = get_current_context()
    buf_string = ' '.join([line for line in buf])
    current_line = buf[row - 1]
    search_string = r'(class|struct) (?P<cname>\w+)[^{{}}]*{{.*{}.*}}'.format(re.escape(current_line))
    match = re.search(search_string, buf_string)
    if match:
        return match.group('cname')
    else:
        return None

# return the position (index) where a function/method name begins in line
# (None if no function/method name is found)
def get_func_name_pos(line):
    match = re.search(r'\S+\(.*\)', line)
    if match:
        return match.start()
    else:
        return None

def insert_include_guard():
    buf, row, _ = get_current_context()
    filename = os.path.basename(buf.name)
    basename, ext = os.path.splitext(filename)
    guard = '{}_{}'.format(basename.upper(), ext.strip('.').upper())
    current_line = buf[row - 1]
    if len(current_line.strip()) == 0:
        del buf[row - 1]
        row -= 1
    new_lines = ['#ifndef {}'.format(guard), '#define {}'.format(guard), '', '#endif // {}'.format(guard)]
    buf.append(new_lines, row)

def switch_hs():
    path = vim.current.buffer.name
    basepath, ext = os.path.splitext(path)
    new_ext = None
    if ext in ['.h', '.hpp']:
        new_ext = '.cpp'
    elif ext == '.cpp':
        if os.path.exists('{}{}'.format(basepath, '.h')):
            new_ext = '.h'
        else:
            new_ext = '.hpp'
    else:
        eprint('{} is no header/source file!?'.format(path))

    to_open = '{}{}'.format(basepath, new_ext)
    vim.command('e {}'.format(to_open))
    return get_current_context()

def create_definition():
    buf, row, _ = get_current_context()
    declaration = buf[row - 1]
    class_name = get_class_name()

    definition = declaration.strip()
    definition = re.sub(r'virtual\s*', '', definition)
    definition = re.sub(r'\s*override', '', definition)
    definition = re.sub(r'\s*final', '', definition)
    definition = re.sub(r';', ' {}', definition)
    if class_name is not None:
        pos = get_func_name_pos(definition)
        definition = definition[:pos] + '{}::'.format(class_name) + definition[pos:]
    buf, _, _ = switch_hs()
    buf.append(definition)
    row = len(buf)
    col = len(buf[row - 1]) - 1
    vim.current.window.cursor = (row, col)
