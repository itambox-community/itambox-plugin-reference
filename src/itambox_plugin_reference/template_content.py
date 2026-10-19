# SPDX-License-Identifier: Apache-2.0
"""Asset detail panel registered through the host template extension point."""

from django.templatetags.static import static
from django.template.loader import render_to_string
from django.utils.html import format_html

from itambox.plugins import get_plugin_config
from itambox.plugins.views import PluginTemplateContent

PLUGIN_NAME = "itambox_plugin_reference"


class ReferenceAssetPanel(PluginTemplateContent):
    models = ["assets.asset"]

    def head(self):
        return format_html(
            '<link rel="stylesheet" href="{}">',
            static("itambox_plugin_reference/plugin.css"),
        )

    def right_panel(self):
        return render_to_string(
            "itambox_plugin_reference/asset_panel.html",
            {
                "display_label": get_plugin_config(PLUGIN_NAME, "display_label"),
                "secret_configured": bool(
                    get_plugin_config(PLUGIN_NAME, "integration_secret")
                ),
            },
        )


template_extensions = [ReferenceAssetPanel]
