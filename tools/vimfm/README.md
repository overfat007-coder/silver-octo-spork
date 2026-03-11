# vimfm

A console two-panel file manager in Go with Vim-like modal commands.

## Features
- two panels rooted in the current working directory
- navigation with `hjkl` or arrow keys
- copy (`yy`), paste (`p`), delete (`dd`)
- file search filter (`/`)
- color highlighting:
  - directories (blue)
  - executables (green)
  - images (magenta)
- human-readable file sizes
- preview for current selection:
  - text files: first 10 lines
  - binary files: header bytes

## Run
```bash
cd tools/vimfm
go run .
```

## Controls
- `q`: quit
- `tab`: switch active panel
- `j`/`k` or `↓`/`↑`: move cursor
- `l`/`→`: enter selected directory
- `h`/`←`: move to parent directory
- `yy`: copy selected file/folder
- `p`: paste into active panel directory
- `dd`: delete selected file/folder
- `/`: search by substring in active panel
- `Esc`: clear active search filter
