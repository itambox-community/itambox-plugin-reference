# SPDX-License-Identifier: Apache-2.0
"""UI routes mounted below the plugin's namespace."""

from django.urls import path

from itambox_plugin_reference.views import ReferenceStatusView

app_name = "itambox_plugin_reference"

urlpatterns = [path("status/", ReferenceStatusView.as_view(), name="status")]
