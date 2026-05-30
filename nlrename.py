#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

CLI tool to rename files using natural language instructions.
Examples:
  nlrename "add today's date to all PDFs" /path/to/files
  nlrename "replace 'draft' with 'final'" /path/to/files --dry-run
  nlrename "all files to lowercase" /path/to/files
"""

import os
import re
import click
from datetime import datetime
from typing import List, Optional


class NaturalLanguageRenamer:
    """Core logic for parsing natural language instructions and renaming files."""

    def __init__(self, instruction: str, dry_run: bool = False):
        self.instruction = instruction.lower()
        self.dry_run = dry_run
        self.date_pattern = r"today's date|current date|date"
        self.case_pattern = r"to (lowercase|uppercase|title case)"
        self.replace_pattern = r"replace ['\"](.*?)['\"] with ['\"](.*?)['\"]"
        self.prefix_suffix_pattern = r"(add|prepend|append) ['\"](.*?)['\"]"

    def parse_instruction(self) -> dict:
        """Parse the natural language instruction into a structured format."""
        result = {
            "action": "none",
            "target": "all",
            "pattern": None,
            "replacement": None,
            "case": None,
            "prefix": None,
            "suffix": None,
        }

        # Date-based renaming
        if re.search(self.date_pattern, self.instruction):
            result["action"] = "date"
            result["target"] = "all"

        # Case transformation
        case_match = re.search(self.case_pattern, self.instruction)
        if case_match:
            result["action"] = "case"
            result["case"] = case_match.group(1)
            result["target"] = "all"

        # Replace text
        replace_match = re.search(self.replace_pattern, self.instruction)
        if replace_match:
            result["action"] = "replace"
            result["pattern"] = replace_match.group(1)
            result["replacement"] = replace_match.group(2)
            result["target"] = "all"

        # Prefix/Suffix
        prefix_suffix_match = re.search(self.prefix_suffix_pattern, self.instruction)
        if prefix_suffix_match:
            action, text = prefix_suffix_match.groups()
            if action in ["add", "prepend"]:
                result["action"] = "prefix"
                result["prefix"] = text
            elif action == "append":
                result["action"] = "suffix"
                result["suffix"] = text
            result["target"] = "all"

        return result

    def generate_new_name(self, filename: str, parsed: dict) -> Optional[str]:
        """Generate the new filename based on the parsed instruction."""
        name, ext = os.path.splitext(filename)
        new_name = name
        new_ext = ext

        if parsed["action"] == "date":
            today = datetime.now().strftime("%Y-%m-%d")
            new_name = f"{today}_{new_name}"

        elif parsed["action"] == "case":
            if parsed["case"] == "lowercase":
                new_name = new_name.lower()
                new_ext = new_ext.lower()
            elif parsed["case"] == "uppercase":
                new_name = new_name.upper()
                new_ext = new_ext.upper()
            elif parsed["case"] == "title case":
                new_name = new_name.title()
                new_ext = new_ext.title()

        elif parsed["action"] == "replace":
            new_name = new_name.replace(parsed["pattern"], parsed["replacement"])

        elif parsed["action"] == "prefix":
            new_name = f"{parsed['prefix']}{new_name}"

        elif parsed["action"] == "suffix":
            new_name = f"{new_name}{parsed['suffix']}"

        return f"{new_name}{new_ext}"

    def rename_files(self, directory: str, file_filter: Optional[str] = None) -> List[str]:
        """Rename files in the directory based on the instruction."""
        parsed = self.parse_instruction()
        renamed = []

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isdir(filepath):
                continue
            if file_filter and file_filter not in filename.lower():
                continue

            new_name = self.generate_new_name(filename, parsed)
            if not new_name or new_name == filename:
                continue

            new_filepath = os.path.join(directory, new_name)
            if not self.dry_run:
                os.rename(filepath, new_filepath)
            renamed.append(f"{filename} -> {new_name}")

        return renamed


@click.command()
@click.argument("instruction", type=str)
@click.argument("directory", type=click.Path(exists=True))
@click.option("--filter", "-f", type=str, help="Filter files by extension or substring (e.g., '.pdf')")
@click.option("--dry-run", is_flag=True, help="Preview changes without renaming")
@click.option("--debug", is_flag=True, help="Enable debug output")
def cli(instruction: str, directory: str, filter: Optional[str], dry_run: bool, debug: bool):
    """CLI entry point for nlrename."""
    if debug:
        click.echo(f"DEBUG: Instruction: {instruction}")
        click.echo(f"DEBUG: Directory: {directory}")
        click.echo(f"DEBUG: Filter: {filter}")
        click.echo(f"DEBUG: Dry run: {dry_run}")

    renamer = NaturalLanguageRenamer(instruction, dry_run)
    renamed = renamer.rename_files(directory, filter)

    if not renamed:
        click.echo("No files matched the instruction.")
        return

    for rename in renamed:
        click.echo(rename)


if __name__ == "__main__":
    cli()