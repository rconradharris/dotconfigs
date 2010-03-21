""" Turn on coloring
syntax on 

""" Desert omits a dark blue so is nice for darkbg 
colorscheme desert

set visualbell

""" Scripting language defaults
set expandtab
set textwidth=78
set wrap

""" Python Convention
set shiftwidth=4
set tabstop=4
map ,sw4 :set ts=4 sw=4<CR>

""" Ruby Convention
set shiftwidth=2
set tabstop=2
map ,sw2 :set ts=2 sw=2<CR>

""" Guess indentation level (when pasting text use :set pastemode)
set autoindent
set smartindent

""" Highlight the tokens that match the search
set hlsearch

""" Start searching after each typed character
set incsearch

""" Ignore the case of the search term when all lowercase
set ignorecase
set smartcase

""" Always maintain at least two lines of context around working-line
set scrolloff=2

""" Present a menu of matching files when using wildcard completion
set wildmenu
set wildmode=list:longest,full
set wildignore=*.pyc

""" Match brackets
set showmatch

""" Show line and column numbers
set ruler

""" When deleting a softtab, delete a shiftwidth number of spaces
set smarttab

""" Reload/edit vimrc easily
map ,rv :so ~/.vimrc<CR>
map ,ev :new ~/.vimrc<CR>

""" Handy git commands
map ,gs :!git status<CR>
map ,gca :!git commit -a<CR>
map ,ga :!git add %<CR>

""" git-diff current file
map ,gd :!git diff --color %<CR>
map ,gdd :!git diff --color<CR>
map ,gdm :!git diff master..<CR>

map ,gb :!git blame %<CR>

""" git-log 
map ,gl :!git log %<CR>
map ,gll :!git log<CR>

""" capistrano deployment
map ,dp :!cap development deploy<CR>
map ,dpm :!cap development deploy:migrations<CR>

""" ctags
map ,bt :!ctags -R .<CR>
set tags=./tags

