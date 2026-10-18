# SPDX-License-Identifier: Apache-2.0
"""Initial schema for the reference plugin's tenant-owned example row."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("organization", "0104_tenant_archive_leaf_markers")]

    operations = [
        migrations.CreateModel(
            name="ReferenceEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=80)),
                ("summary", models.CharField(blank=True, max_length=240)),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reference_plugin_entries",
                        to="organization.tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "Reference entry",
                "verbose_name_plural": "Reference entries",
                "ordering": ("label",),
            },
        ),
    ]
