# Natural Language File Renamer (nlrename)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool to rename files using natural language instructions. No AI, no APIs — just regex, dates, and case transformations.

## Features
- Rename files using natural language (e.g., `"add today's date to all PDFs"`).
- Supports regex, date patterns, and case transformations.
- Dry-run mode for previewing changes.
- Filter files by extension or substring.

## Installation
```bash
pip install --user click python-dateutil
chmod +x nlrename.py
sudo ln -s $(pwd)/nlrename.py /usr/local/bin/nlrename
```

## Usage
```bash
# Add today's date to all PDFs
nlrename "add today's date to all PDFs" /path/to/files --filter ".pdf"

# Replace 'draft' with 'final' (dry run)
nlrename "replace 'draft' with 'final'" /path/to/files --dry-run

# Convert all filenames to lowercase
nlrename "all files to lowercase" /path/to/files
```

## Examples
| Instruction                          | Before               | After                     |
|-------------------------------------|----------------------|---------------------------|
| `"add today's date to all PDFs"`   | `report.pdf`         | `2026-05-30_report.pdf`    |
| `"replace 'draft' with 'final'"`   | `draft_report.pdf`   | `final_report.pdf`         |
| `"all files to lowercase"`        | `DRAFT_REPORT.PDF`   | `draft_report.pdf`         |

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

## License
MIT