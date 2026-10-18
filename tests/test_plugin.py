# SPDX-License-Identifier: Apache-2.0
"""Integration checks executed with the host's supported plugin verifier."""

import unittest

from itambox.plugins.testing import verify_plugins


class ReferencePluginManifestTests(unittest.TestCase):
    def test_host_verifies_installed_plugin_and_compatibility_manifest(self):
        report = verify_plugins("itambox_plugin_reference")

        self.assertIn("itambox_plugin_reference", report.active)
        manifest = report.plugins["itambox_plugin_reference"]
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertEqual(manifest["itambox_range"], ">=1.0,<1.1")
