if !has("python") && !has("python3")
    echo "vim has to be compiled with +python[3] to run this"
    finish
endif

if exists('g:tinycpp_plugin_loaded')
    finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

function! s:UsingPython3()
  if has('python3')
    return 1
  endif
  return 0
endfunction

let s:using_python3 = s:UsingPython3()
let s:python_until_eof = s:using_python3 ? "python3 << EOF" : "python << EOF"
let s:python_command = s:using_python3 ? "python3 " : "python "

" setup python
exec s:python_until_eof
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import tinycpp as cpp
EOF

" function for inserting include guard
function! TcIncGuard()
    exec s:python_command "cpp.insert_include_guard()"
endfunction
command! -nargs=0 TcIncGuard call TcIncGuard()

" function for switching between header and source file
function! TcSwitchHS()
    exec s:python_command "cpp.switch_hs()"
endfunction
command! -nargs=0 TcSwitchHS call TcSwitchHS()

" function for creating definition of function/method in source file
function! TcCreateDef()
    exec s:python_command "cpp.create_definition()"
endfunction
command! -nargs=0 TcCreateDef call TcCreateDef()

" function for creating definition of function/method in source file
function! TcMoveDef()
    exec s:python_command "cpp.move_definition()"
endfunction
command! -nargs=0 TcMoveDef call TcMoveDef()

let g:tinycpp_plugin_loaded = 1

