# SPDX-License-Identifier: Apache-2.0
"""Small example model that uses the host's tenant-scoped manager."""

from django.db import models

from core.managers import TenantScopingManager


class ReferenceEntry(models.Model):
    """A tenant-owned row used to exercise plugin model integration."""

    objects = TenantScopingManager()

    tenant = models.ForeignKey(
        "organization.Tenant",
        on_delete=models.CASCADE,
        related_name="reference_plugin_entries",
    )
    label = models.CharField(max_length=80)
    summary = models.CharField(max_length=240, blank=True)

    class Meta:
        ordering = ("label",)
        verbose_name = "Reference entry"
        verbose_name_plural = "Reference entries"

    def __str__(self):
        return self.label
