# SPDX-License-Identifier: Apache-2.0
"""Package layout and CSP safety checks for browser-delivered plugin assets."""

import re
import unittest
from pathlib import Path

import itambox_plugin_reference


PACKAGE_ROOT = Path(itambox_plugin_reference.__file__).parent
INLINE_STYLE = re.compile(r"\bstyle\s*=\s*['\"]", re.IGNORECASE)
INLINE_STYLE_ELEMENT = re.compile(r"<style\b", re.IGNORECASE)
INLINE_SCRIPT = re.compile(r"<script\b", re.IGNORECASE)


class ReferencePluginAssetTests(unittest.TestCase):
    def test_templates_and_static_files_are_namespaced_and_shipped(self):
        template_root = PACKAGE_ROOT / "templates" / "itambox_plugin_reference"
        static_file = (
            PACKAGE_ROOT / "static" / "itambox_plugin_reference" / "plugin.css"
        )

        self.assertTrue((template_root / "status.html").is_file())
        self.assertTrue((template_root / "asset_panel.html").is_file())
        self.assertTrue(static_file.is_file())
        self.assertIn(".reference-status", static_file.read_text(encoding="utf-8"))

    def test_browser_templates_and_html_emitters_do_not_use_inline_csp_exceptions(self):
        source_paths = [
            *(PACKAGE_ROOT / "templates" / "itambox_plugin_reference").glob("*.html"),
            PACKAGE_ROOT / "template_content.py",
            PACKAGE_ROOT / "views.py",
        ]

        for path in source_paths:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(
                    INLINE_STYLE.search(text), f"{path} contains a style attribute"
                )
                self.assertIsNone(
                    INLINE_STYLE_ELEMENT.search(text),
                    f"{path} contains an inline style element",
                )
                self.assertIsNone(
                    INLINE_SCRIPT.search(text),
                    f"{path} contains an inline script element",
                )
