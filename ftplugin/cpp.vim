if !has("python")
    echo "vim has to be compiled with +python to run this"
    finish
endif

if exists('g:tinycpp_plugin_loaded')
    finish
endif

let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" setup python
python << EOF
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
    python cpp.insert_include_guard()
endfunction
command! -nargs=0 TcIncGuard call TcIncGuard()

" function for switching between header and source file
function! TcSwitchHS()
    python cpp.switch_hs()
endfunction
command! -nargs=0 TcSwitchHS call TcSwitchHS()

" function for creating definition of function/method in source file
function! TcCreateDef()
    python cpp.create_definition()
endfunction
command! -nargs=0 TcCreateDef call TcCreateDef()

let g:tinycpp_plugin_loaded = 1
