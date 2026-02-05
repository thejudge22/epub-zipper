# ePub Folder Converter

A simple Python utility to convert ePub folders (directories with `.epub` extension containing ePub formatted content) into proper ePub files.

## What it does

Many eBook management tools and extractors create folders named `bookname.epub/` containing the unpacked ePub contents (mimetype, META-INF, OEBPS, etc.). This script batch converts those folders back into actual `.epub` files (which are ZIP archives with specific internal structure).

## Features

- ✅ Batch converts all `.epub` folders in a directory
- ✅ Preserves proper ePub internal structure (mimetype at root level)
- ✅ Outputs to separate `converted/` subdirectory to avoid naming conflicts
- ✅ Optional cleanup: remove source folders after successful conversion
- ✅ Dry-run mode to preview changes before executing
- ✅ Cross-platform (Windows, macOS, Linux)

## Requirements

- Python 3.6+

No external dependencies required (uses standard library only).

## Installation

1. Clone this repository or download `convert_epub.py`
2. python3 ./convert_epub.py
