# SPDX-License-Identifier: Apache-2.0
"""Views for the reference plugin's small UI surface."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from itambox.plugins import get_plugin_config

PLUGIN_NAME = "itambox_plugin_reference"


class ReferenceStatusView(LoginRequiredMixin, TemplateView):
    template_name = "itambox_plugin_reference/status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["display_label"] = get_plugin_config(PLUGIN_NAME, "display_label")
        context["secret_configured"] = bool(
            get_plugin_config(PLUGIN_NAME, "integration_secret")
        )
        return context
