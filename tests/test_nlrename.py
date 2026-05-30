#!/usr/bin/env python3
"""
Unit tests for nlrename.py
Run with: pytest tests/
"""

import os
import pytest
from datetime import datetime
from nlrename import NaturalLanguageRenamer


def test_parse_instruction_date():
    renamer = NaturalLanguageRenamer("add today's date to all files")
    parsed = renamer.parse_instruction()
    assert parsed["action"] == "date"
    assert parsed["target"] == "all"


def test_parse_instruction_case():
    renamer = NaturalLanguageRenamer("all files to lowercase")
    parsed = renamer.parse_instruction()
    assert parsed["action"] == "case"
    assert parsed["case"] == "lowercase"


def test_parse_instruction_replace():
    renamer = NaturalLanguageRenamer("replace 'draft' with 'final'")
    parsed = renamer.parse_instruction()
    assert parsed["action"] == "replace"
    assert parsed["pattern"] == "draft"
    assert parsed["replacement"] == "final"


def test_generate_new_name_date(tmp_path):
    today = datetime.now().strftime("%Y-%m-%d")
    renamer = NaturalLanguageRenamer("add today's date")
    parsed = renamer.parse_instruction()
    new_name = renamer.generate_new_name("report.pdf", parsed)
    assert new_name == f"{today}_report.pdf"


def test_generate_new_name_case(tmp_path):
    renamer = NaturalLanguageRenamer("all files to lowercase")
    parsed = renamer.parse_instruction()
    new_name = renamer.generate_new_name("DRAFT_REPORT.PDF", parsed)
    assert new_name == "draft_report.pdf"


if __name__ == "__main__":
    pytest.main(["-v", __file__])