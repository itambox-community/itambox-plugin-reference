# SPDX-License-Identifier: Apache-2.0
"""Host-authorized read-only API viewset."""

from itambox.api.viewsets import ITAMBoxReadOnlyModelViewSet
from itambox_plugin_reference.models import ReferenceEntry
from itambox_plugin_reference.serializers import ReferenceEntrySerializer


class ReferenceEntryViewSet(ITAMBoxReadOnlyModelViewSet):
    queryset = ReferenceEntry.objects.all()
    serializer_class = ReferenceEntrySerializer


viewsets = [("entries", ReferenceEntryViewSet, "reference-entries")]
