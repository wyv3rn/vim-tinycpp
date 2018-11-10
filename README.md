# vim-tinycpp
Vim plugin for not many (hence tiny) but useful convenience functionalities when developing C++

## Installation

Your best bet is to use some plugin manager like [Vundle](https://github.com/VundleVim/Vundle.vim) or [vim-plug](https://github.com/junegunn/vim-plug).
Example for Vundle: Add `Plugin 'wyv3rn/vim-tinycpp'` to your `.vimrc`.

## Current features

See `help tinycpp` for more info on usage.

* Add include guard to current buffer (`:TcIncGuard`)

Wow, that's really tiny ... (but hopefully some more functionalities will follow, see below)

## Planned features

* Generate (empty) function/method definition based on declaration
* Refactor function/method signature: If you changed the signature in one of declaration/definition, tinycpp should help you adopting the other

