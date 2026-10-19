# SPDX-License-Identifier: Apache-2.0
"""Standalone item contributed to the shared Plugins navigation."""

from itambox.plugins.navigation import PluginNavigationItem


class ReferencePluginNavigationItem(PluginNavigationItem):
    link = "plugins:itambox_plugin_reference:status"
    link_text = "Reference plugin"
    auth_required = True


menu_items = [ReferencePluginNavigationItem]
