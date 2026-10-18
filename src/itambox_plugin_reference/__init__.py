# SPDX-License-Identifier: Apache-2.0
"""Reference plugin package and its host-discovered manifest."""

from itambox.plugins import PluginConfig

__version__ = "0.1.0"


class ReferencePluginConfig(PluginConfig):
    """Manifest for the independently installed reference plugin."""

    name = "itambox_plugin_reference"
    verbose_name = "Reference plugin"
    description = "A small example covering the stable plugin extension points."
    version = __version__
    author = "ITAMbox Community"
    itambox_range = ">=1.0,<1.1"
    base_url = "itambox_plugin_reference"
    settings_schema = {
        "display_label": {"type": "str", "required": True},
        "integration_secret": {"type": "str", "secret": True},
    }


config = ReferencePluginConfig
