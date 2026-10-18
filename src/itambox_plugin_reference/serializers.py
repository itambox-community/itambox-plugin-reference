# SPDX-License-Identifier: Apache-2.0
"""REST representation of the reference entry."""

from rest_framework import serializers

from itambox_plugin_reference.models import ReferenceEntry


class ReferenceEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceEntry
        fields = ("id", "tenant", "label", "summary")
        read_only_fields = fields
