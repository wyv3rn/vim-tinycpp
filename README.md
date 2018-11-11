# TinyC++
TinyC++ is a Vim plugin for not many (hence tiny) but useful convenience functionalities when developing C++.

Other plugins I personally use in this context are [YouCompleteMe](https://github.com/Valloric/YouCompleteMe) and [UltiSnips](https://github.com/SirVer/ultisnips).

## Installation

Your best bet is to use some plugin manager like [Vundle](https://github.com/VundleVim/Vundle.vim) or [vim-plug](https://github.com/junegunn/vim-plug).

Example for Vundle: Add `Plugin 'wyv3rn/vim-tinycpp'` to your `vimrc`.

As the plugin is only loaded for the `cpp` filetype, you have to enable the filetype plugin, e.g. by inserting `filetype plugin on` in your `vimrc`.
Furthermore, your Vim must be compiled with Python support.

## Current features

See `:help tinycpp` for more info on usage.
TLDR: Use it by invoking commands (`:Tc...`); freely map those to your desire.

* Add include guard to current buffer (`:TcIncGuard`)
* Switch between header and source file (`:TcSwitchHS`)
* Create definition for function/method declaration in source file (`:TcCreateDef`)

Wow, that's really tiny ... (but hopefully some more functionalities will follow, see below)

## Planned features

* Refactor function/method signature: If you changed the signature in one of declaration/definition, tinycpp should help you adopting the other
* For a "combined" function/method declaration and definition: move definition to source file (and maybe the opposite, i.e. merge definition with declaration)

