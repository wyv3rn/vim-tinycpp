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
    brace_count = 0
    i = row - 1
    while i >= 0:
        brace_count += buf[i].count('{')
        brace_count -= buf[i].count('}')
        if brace_count == 1:
            # seems like we found the beginning of our block -> search non empty line before it
            class_def_line = buf[i].replace('{', '')
            while not class_def_line.strip() and i > 0:
                i -= 1
                class_def_line = buf[i]
            match = re.search(r'(class|struct)\s+(?P<cname>\w+)', class_def_line)
            if match:
                return match.group('cname')
            else:
                # seems like our block was not a class def after all
                return None
        i -= 1
    return None

# from the current position, return next { ... } block as well as its start and end index
# None, -1, -1 if no block is found
def get_next_block():
    buf, row, _ = get_current_context()
    block = []
    i = row - 1
    brace_count = 0
    start = -1
    while i < len(buf):
        current_line = buf[i]
        if current_line.count('{') == 1:
            start = i
            current_line = current_line[current_line.find('{'):]
            if current_line.count('}') == 1:
            # inline block
                return [current_line], i, i
        if start != -1:
            block.append(current_line)
            brace_count += buf[i].count('{')
            brace_count -= buf[i].count('}')
        if start != -1 and brace_count == 0:
            return block, start, i
        i += 1
    return None, -1, -1

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
    new_lines = ['#ifndef {}'.format(guard), '#define {}'.format(guard), '', '', '', '#endif // {}'.format(guard)]
    buf.append(new_lines, row)
    vim.command('normal! 3j')

def switch_hs():
    path = vim.current.buffer.name
    basepath, ext = os.path.splitext(path)
    new_ext = None
    if ext in ['.h', '.hpp']:
        if os.path.exists('{}{}'.format(basepath, '.cc')):
            new_ext = '.cc'
        else:
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

def move_definition():
    buf, row, _ = get_current_context()
    ext = os.path.splitext(buf.name)[1]
    block, start, end = get_next_block()
    if block is None:
        eprint('No block found to move')
        return

    if len(block) > 1:
        del(block[0]) # don't need opening brace as it is created by create_definition anyway

    brace_pos = buf[start].find('{')
    delete_start = start
    if(brace_pos != 0):
        buf[start] = buf[start][:brace_pos].rstrip() + ';'
        delete_start += 1

    del buf[delete_start:end+1]
    # save to savely switch file (in create_definition)
    vim.command('w')

    create_definition()
    # switched file, so refresh context
    buf, row, _ = get_current_context()
    if len(block) > 1:
        vim.command('normal! x')
        # insert block and auto-align
        buf.append(block, row)
        vim.command(str(row))
        vim.command('normal! V | {0}j | = | V | {0}j'.format(len(block)))
    else:
        # just append the one-lined block to the end of the signature (after deleting the braces from create_definition)
        vim.command('normal! x')
        vim.command('normal! x')
        buf[row - 1] = buf[row - 1] + block[0]

