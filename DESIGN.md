# Natural Language File Renamer: Design Document

## Overview
`nlrename` is a CLI tool to rename files using natural language instructions. It parses instructions like `"add today's date to all PDFs"` and applies transformations using regex, date patterns, and case logic.

## Architecture
```
┌───────────────────────┐    ┌───────────────────────┐    ┌───────────────────────┐
│   NaturalLanguageRenamer  │    │       click CLI       │    │    File System        │
│  (Core Logic)          │───▶│  (User Interface)     │───▶│  (os.rename)          │
└───────────────────────┘    └───────────────────────┘    └───────────────────────┘
```

### Components
1. **Parser**: Converts natural language to structured actions (e.g., `"add today's date"` → `{"action": "date", "target": "all"}`).
2. **Transformer**: Applies transformations (date, case, regex, prefix/suffix).
3. **CLI**: `click`-based interface for user input/output.

## Instruction Parsing
| Instruction Pattern               | Action   | Example Output               |
|----------------------------------|----------|-------------------------------|
| `today's date`                   | `date`   | `2026-05-30_filename.ext`     |
| `to lowercase`                   | `case`   | `filename.ext`                |
| `replace 'X' with 'Y'`           | `replace`| `filename_Y.ext`              |
| `add 'prefix'`                   | `prefix` | `prefix_filename.ext`         |

## Edge Cases
- **Case Sensitivity**: Instructions are case-insensitive (e.g., `"TO LOWERCASE"` works).
- **File Extensions**: Case transformations apply to both name and extension (e.g., `.PDF` → `.pdf`).
- **Dry Run**: Preview changes without renaming.

## Limitations
- No AI or external APIs (pure regex/date logic).
- No undo functionality (use `--dry-run` first).

## Future Work
- Add `--undo` flag to revert changes.
- Support custom date formats (e.g., `"add date as DD-MM-YYYY"`).