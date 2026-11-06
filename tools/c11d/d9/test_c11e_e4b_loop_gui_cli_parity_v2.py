#!/usr/bin/env python3
"""Unit tests for the E4B Loop populated GUI/CLI Unicode parity helper."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e4b_loop_gui_cli_parity_v2 as parity


class E4BLoopGuiCliParityV2Tests(unittest.TestCase):
    def test_exact_four_field_fixture(self):
        self.assertEqual(set(parity.EXPECTED_EDITORIAL), set(parity.FIELDS))
        self.assertEqual(parity.validate_editorial(dict(parity.EXPECTED_EDITORIAL), "fixture"), parity.EXPECTED_EDITORIAL)

    def test_utf8_fixture_contains_spanish_codepoints(self):
        self.assertIn(chr(0x00ED), parity.EXPECTED_EDITORIAL["title"])
        self.assertIn(chr(0x2014), parity.EXPECTED_EDITORIAL["title"])
        self.assertIn(chr(0x00F3), parity.EXPECTED_EDITORIAL["subtitle"])
        self.assertIn(chr(0x00E9), parity.EXPECTED_EDITORIAL["subtitle"])

    def test_mojibake_is_rejected(self):
        with self.assertRaises(parity.ParityError):
            parity.assert_no_mojibake("T\u00c3\u00adtulo", "fixture.title")

    def test_missing_or_extra_editorial_keys_are_rejected(self):
        with self.assertRaises(parity.ParityError):
            parity.validate_editorial({"title": parity.EXPECTED_EDITORIAL["title"]}, "missing")
        extra = dict(parity.EXPECTED_EDITORIAL)
        extra["unused"] = "not_allowed"
        with self.assertRaises(parity.ParityError):
            parity.validate_editorial(extra, "extra")

    def test_nfc_normalization_is_required(self):
        with self.assertRaises(parity.ParityError):
            parity.assert_no_mojibake("a\u0301", "decomposed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
