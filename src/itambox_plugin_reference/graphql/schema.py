# SPDX-License-Identifier: Apache-2.0
"""Read-only GraphQL query for tenant-scoped reference entries."""

import strawberry
from django.core.exceptions import PermissionDenied

from itambox_plugin_reference.models import ReferenceEntry

PLUGIN_PERMISSION = "itambox_plugin_reference.view_referenceentry"


def _request_from_info(info):
    context = info.context
    request = getattr(context, "request", None)
    if request is None and isinstance(context, dict):
        request = context.get("request")
    return request if request is not None else context


@strawberry.type
class ReferenceEntryResult:
    id: strawberry.ID
    label: str
    summary: str


@strawberry.type
class Query:
    @strawberry.field
    def reference_entries(self, info: strawberry.Info) -> list[ReferenceEntryResult]:
        request = _request_from_info(info)
        user = getattr(request, "user", None)
        if (
            not user
            or not user.is_authenticated
            or not user.has_perm(PLUGIN_PERMISSION)
        ):
            raise PermissionDenied("Permission denied.")

        return [
            ReferenceEntryResult(id=str(row.pk), label=row.label, summary=row.summary)
            for row in ReferenceEntry.objects.all()
        ]
