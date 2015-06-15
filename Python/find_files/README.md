## Find Files with Specific Surfixes 

This short python script is used for copying files with specific surfixes from 

source directory and all its subdirectories to destination directory.

## Basic Usage

- `python find_files.py -h`
  - This will print out all options and minimum directions.

- `python find_files.py -f src -t dest`
  - copy all files with surfix `png`, `jepg`, `gif` and `jpg` from `src` (directory) to `dest` (directory).
  - you can specify surfixes you want using `-s` or `--surfixes` option.
  - ex: `python find_files.py -f src -t dest -s md` (Copy all markdown files).
