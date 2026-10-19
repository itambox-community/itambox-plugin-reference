# SPDX-License-Identifier: Apache-2.0
"""Integration checks against the host's supported plugin test helper."""

import json
import unittest

from django.test import SimpleTestCase, override_settings

from itambox.plugins.testing import PluginVerificationError, verify_plugins

PLUGIN_NAME = "itambox_plugin_reference"


class ReferencePluginContractTests(SimpleTestCase):
    def test_host_verifies_every_declared_extension_point(self):
        report = verify_plugins(
            PLUGIN_NAME,
            environ={
                "ITAMBOX_PLUGINS_CONFIG": json.dumps(
                    {PLUGIN_NAME: {"display_label": "Plugin CI"}}
                ),
                "ITAMBOX_PLUGIN_ITAMBOX_PLUGIN_REFERENCE_INTEGRATION_SECRET": "test-only-not-a-credential",
            },
        )

        self.assertEqual(report.active, (PLUGIN_NAME,))
        plugin = report.plugins[PLUGIN_NAME]
        self.assertEqual(
            set(plugin["registered"]),
            {
                "template_extensions",
                "menu_items",
                "viewsets",
                "permission_targets",
                "graphql_schema",
            },
        )
        self.assertTrue(plugin["ui"])
        self.assertEqual(plugin["api_prefixes"], ["entries"])

    def test_missing_required_plain_setting_is_rejected_by_the_host(self):
        with self.assertRaises(PluginVerificationError) as caught:
            verify_plugins(PLUGIN_NAME)

        self.assertEqual(caught.exception.plugin, PLUGIN_NAME)
        self.assertEqual(caught.exception.phase, "resolve")
        self.assertIn("display_label", caught.exception.detail)

    def test_model_permission_target_is_added_to_the_role_matrix(self):
        from django.apps import apps

        from organization.forms.role_matrix import build_matrix_models

        model = apps.get_model(PLUGIN_NAME, "ReferenceEntry")
        key = f"plugin_{len(model._meta.app_label)}_{model._meta.app_label}_{model._meta.model_name}"
        matrix = build_matrix_models()

        self.assertIn(key, matrix)
        self.assertEqual(matrix[key]["app"], PLUGIN_NAME)
        self.assertEqual(matrix[key]["model_name"], "referenceentry")

    @override_settings(
        PLUGINS_RESOLVED_CONFIG={
            PLUGIN_NAME: {
                "display_label": "Panel test",
                "integration_secret": "panel-only-test-value",
            }
        }
    )
    def test_asset_detail_panel_renders_namespaced_html_and_external_css(self):
        from django.template import Context

        from core.templatetags.plugins import plugin_template_content

        context = Context({"request": None})
        panel = plugin_template_content(
            context, "assets.asset", "right_panel", object()
        )
        head = plugin_template_content(context, "assets.asset", "head", object())

        self.assertIn("Reference panel", str(panel))
        self.assertIn("Panel test", str(panel))
        self.assertIn("Secret setting configured.", str(panel))
        self.assertNotIn("panel-only-test-value", str(panel))
        self.assertIn("/static/itambox_plugin_reference/plugin.css", str(head))


if __name__ == "__main__":
    unittest.main()
