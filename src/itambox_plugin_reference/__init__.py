# SPDX-License-Identifier: Apache-2.0
"""Reference plugin package and its host-discovered manifest."""

from itambox.plugins import PluginConfig

__version__ = "0.1.0"


class ReferencePluginConfig(PluginConfig):
    """Manifest for the independently installed reference plugin."""

    name = "itambox_plugin_reference"
    verbose_name = "Reference plugin"
    description = "A separately installable reference plugin package."
    version = __version__
    author = "ITAMbox Community"
    itambox_range = ">=1.0,<1.1"


config = ReferencePluginConfig
