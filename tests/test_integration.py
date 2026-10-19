# SPDX-License-Identifier: Apache-2.0
"""Database-backed tenant and token permission checks for the plugin endpoint."""

import json

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.migrations.loader import MigrationLoader
from django.test import TestCase, override_settings

from core.managers import set_current_membership, set_current_tenant
from core.tests.mixins import TenantTestMixin, grant
from itambox_plugin_reference.models import ReferenceEntry
from organization.models import Role, Tenant
from users.models import Token

PLUGIN_NAME = "itambox_plugin_reference"
VIEW_PERMISSION = f"{PLUGIN_NAME}.view_referenceentry"


class ReferenceEntryIntegrationTests(TenantTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.setup_tenant_context(
            name="Plugin tenant A",
            slug="plugin-tenant-a",
            permissions=[VIEW_PERMISSION],
        )
        self.other_tenant = Tenant.objects.create(
            name="Plugin tenant B", slug="plugin-tenant-b"
        )
        self.own_entry = ReferenceEntry._base_manager.create(
            tenant=self.tenant,
            label="Tenant A entry",
            summary="Visible only in tenant A",
        )
        self.foreign_entry = ReferenceEntry._base_manager.create(
            tenant=self.other_tenant,
            label="Tenant B entry",
            summary="Must not cross the tenant boundary",
        )

    def tearDown(self):
        set_current_membership(None)
        set_current_tenant(None)
        super().tearDown()

    def test_token_reads_only_its_tenant_and_requires_model_view_permission(self):
        token = Token.objects.create(user=self.tenant_user, tenant=self.tenant)
        path = "/api/plugins/itambox_plugin_reference/entries/"

        response = self.client.get(path, HTTP_AUTHORIZATION=f"Token {token.key}")

        self.assertEqual(response.status_code, 200, response.content.decode())
        payload = response.json()
        rows = payload["results"] if isinstance(payload, dict) else payload
        self.assertEqual([row["label"] for row in rows], ["Tenant A entry"])
        self.assertEqual(rows[0]["tenant"], self.tenant.pk)

        foreign_detail = self.client.get(
            f"{path}{self.foreign_entry.pk}/",
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )
        self.assertEqual(foreign_detail.status_code, 404)

        denied_user = get_user_model().objects.create_user(
            username="plugin_token_without_view_permission",
            password="test-password",
        )
        denied_role = Role.objects.create(
            tenant=self.tenant, name="No plugin view permission", permissions=[]
        )
        grant(denied_user, self.tenant, denied_role)
        denied_token = Token.objects.create(user=denied_user, tenant=self.tenant)
        denied_response = self.client.get(
            path, HTTP_AUTHORIZATION=f"Token {denied_token.key}"
        )
        self.assertEqual(denied_response.status_code, 403)

        write_response = self.client.post(
            path,
            data={"label": "must not be created", "summary": "read-only endpoint"},
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )
        self.assertEqual(write_response.status_code, 403)
        self.assertFalse(
            ReferenceEntry._base_manager.filter(label="must not be created").exists()
        )

    def test_graphql_query_is_read_only_permission_gated_and_tenant_scoped(self):
        token = Token.objects.create(user=self.tenant_user, tenant=self.tenant)
        response = self.client.post(
            "/graphql/",
            data=json.dumps({"query": "{ referenceEntries { label summary } }"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

        self.assertEqual(response.status_code, 200, response.content.decode())
        body = response.json()
        self.assertNotIn("errors", body)
        self.assertEqual(
            body["data"]["referenceEntries"],
            [{"label": "Tenant A entry", "summary": "Visible only in tenant A"}],
        )
        self.assertNotIn("Tenant B entry", response.content.decode())

        denied_user = get_user_model().objects.create_user(
            username="plugin_graphql_without_view_permission",
            password="test-password",
        )
        denied_role = Role.objects.create(
            tenant=self.tenant, name="No GraphQL view permission", permissions=[]
        )
        grant(denied_user, self.tenant, denied_role)
        denied_token = Token.objects.create(user=denied_user, tenant=self.tenant)
        denied_response = self.client.post(
            "/graphql/",
            data=json.dumps({"query": "{ referenceEntries { label } }"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {denied_token.key}",
        )
        self.assertEqual(denied_response.status_code, 200)
        denied_body = denied_response.json()
        self.assertTrue(denied_body.get("errors"))
        self.assertIn("Permission denied", denied_body["errors"][0]["message"])

        anonymous_response = self.client.post(
            "/graphql/",
            data=json.dumps({"query": "{ referenceEntries { label } }"}),
            content_type="application/json",
        )
        self.assertEqual(anonymous_response.status_code, 401)
        self.assertNotIn("Tenant A entry", anonymous_response.content.decode())

    @override_settings(
        PLUGINS_RESOLVED_CONFIG={
            PLUGIN_NAME: {
                "display_label": "Visible status",
                "integration_secret": "never-render-this-value",
            }
        }
    )
    def test_authenticated_ui_page_reports_secret_presence_without_exposing_value(self):
        path = "/plugins/itambox_plugin_reference/status/"
        anonymous_response = self.client.get(path)
        self.assertEqual(anonymous_response.status_code, 302)

        self.client.force_login(self.tenant_user)
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visible status")
        self.assertContains(response, "Secret setting configured.")
        self.assertNotContains(response, "never-render-this-value")

    def test_model_migration_is_present_and_has_no_reverse_core_foreign_key(self):
        loader = MigrationLoader(None, ignore_no_migrations=True)
        node = (PLUGIN_NAME, "0001_initial")
        migration = loader.disk_migrations[node]
        model = ReferenceEntry

        self.assertTrue(migration.initial)
        self.assertIn(
            ("organization", "0104_tenant_archive_leaf_markers"), migration.dependencies
        )
        self.assertEqual(model._meta.app_label, PLUGIN_NAME)
        self.assertEqual(
            model._meta.get_field("tenant").remote_field.model._meta.app_label,
            "organization",
        )
        plugin_relations = [
            (field.name, field.remote_field.model._meta.label)
            for field in model._meta.local_fields
            if getattr(field, "remote_field", None) is not None
        ]
        self.assertEqual(plugin_relations, [("tenant", "organization.Tenant")])

        host_foreign_keys = [
            f"{host_model._meta.label}.{field.name}"
            for host_model in apps.get_models()
            if host_model._meta.app_label != PLUGIN_NAME
            for field in host_model._meta.get_fields()
            if not field.auto_created
            and getattr(field, "remote_field", None) is not None
            and field.remote_field.model is model
        ]
        self.assertEqual(host_foreign_keys, [])
        self.assertTrue(
            Permission.objects.filter(
                content_type__app_label=PLUGIN_NAME,
                codename="view_referenceentry",
            ).exists()
        )
