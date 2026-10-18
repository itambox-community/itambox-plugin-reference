# Reference plugin

A separately installable reference package for extending an ITAMbox deployment. The plugin is a trusted, in-process Django application: install it only from a source you trust.

- Distribution: `itambox-plugin-reference`
- Python import / plugin name: `itambox_plugin_reference`
- Supported product range: `>=1.0,<1.1` (all patch releases in 1.0; no separate plugin API version)
- License: Apache-2.0

## Install

After a package release is published to PyPI:

```sh
pip install itambox-plugin-reference
```

Until the first PyPI publication, install the wheel attached to a GitHub Release, or build one from a source archive:

```sh
uv build --wheel
pip install dist/itambox_plugin_reference-0.1.0-py3-none-any.whl
```

The plugin is a Python package; a deployment does not need a checkout of the host or this repository. Restart the host after changing installed plugins.

## Enable and configure

Add the package name to the host's `PLUGINS` setting (or the `ITAMBOX_PLUGINS` environment variable):

```python
PLUGINS = ["itambox_plugin_reference"]
```

The required plain setting is supplied in `ITAMBOX_PLUGINS_CONFIG`. The optional secret setting is declared as secret in the schema and should be supplied through the deployment's secret-management channel using its per-key override:

```sh
ITAMBOX_PLUGINS_CONFIG='{"itambox_plugin_reference":{"display_label":"Reference status"}}'
ITAMBOX_PLUGIN_ITAMBOX_PLUGIN_REFERENCE_INTEGRATION_SECRET='<injected-by-secret-manager>'
```

The UI and asset panel report only whether the secret setting is configured; they never render its value. Do not put real secrets in source control.

## Extension points in this package

The implementation is pinned to the host code revision used by CI and verified with its executable plugin test helper. The host's versioned API Reference marks the manifest, settings schema, template/menu/viewset/GraphQL declarations, URLconf, permission targets, and verification helper Stable. The example's plugin-owned model is required by #872, but the host's tenant-scoping manager is not part of that Stable plugin API inventory; pin the host revision and requalify before changing it. The documentation's broader getting-started text still calls the plugin system Experimental, so this package does not make a wider stability claim.

| Extension point | Example in this package | Host documentation |
|---|---|---|
| Tenant-owned model and migration | `models.py`, `migrations/0001_initial.py`; the model uses the host tenant-scoped manager and references the host tenant, with no host table referencing the plugin model | [Tenant model guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/models/organization/tenant.md), [pinned tenant manager source](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/core/managers.py) |
| Asset detail template panel | `template_content.py` and the namespaced `templates/itambox_plugin_reference/asset_panel.html` | [Template injection guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/hooks.md#1-template-injection), [pinned composition source](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/assembly.py) |
| Shared Plugins navigation item | `navigation.py` | [Navigation guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/hooks.md#2-sidebar-navigation), [pinned composition source](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/assembly.py) |
| Plugin UI route | `urls.py` and `views.py`, mounted under `/plugins/itambox_plugin_reference/` | [UI routing guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/hooks.md#3-web-ui-routing), [pinned URL assembly source](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/urls.py) |
| Read-only REST endpoint | `api/viewsets.py` and `serializers.py`, mounted under `/api/plugins/itambox_plugin_reference/entries/` | [REST resources guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/hooks.md#4-rest-api-resources), [Stable API contract](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/api_reference.md#extension-points), [pinned viewset source](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/api/viewsets.py) |
| GraphQL query | `graphql/schema.py`; query-only and protected by the model view permission | [GraphQL guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/hooks.md#5-graphql-schema-extension), [pinned composition source](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/assembly.py) |
| Role-matrix permission target | `permissions.py` declares the plugin-owned model | [Permission targets in the API Reference](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/api_reference.md#extension-points), [pinned permission-target validation](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/assembly.py), [role matrix](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/organization/forms/role_matrix.py) |
| Required and secret settings | `settings_schema` in the plugin manifest; values are read through `get_plugin_config` | [Configuration guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/api_reference.md#configuration), [pinned settings schema and secret handling](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/settings_schema.py), [pinned configuration accessor](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/__init__.py) |
| Namespaced templates and static assets | `templates/itambox_plugin_reference/` and `static/itambox_plugin_reference/`; the panel loads an external stylesheet without inline style or script | [Template injection guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/plugins/hooks.md#1-template-injection), [deployment security guide](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/docs/security/deployment-security.md) |

The tests verify plugin composition through `itambox.plugins.testing.verify_plugins`, exercise tenant and token boundaries over real HTTP requests, check the role matrix and GraphQL query, and verify package assets. CI also runs the host's template linter and the plugin's CSP assertions. The pinned implementation's manifest and configuration contract lives in [`PluginConfig`](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/__init__.py) and its [test helper](https://github.com/itambox-community/itambox-webapp/blob/b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3/itambox/itambox/plugins/testing.py).

## Compatibility

The manifest declares one product compatibility range, `>=1.0,<1.1`. This accepts patch releases within 1.0 and intentionally does not declare a separate plugin API version. The plugin's own release version is independent of the product range.

The current CI host pin is the exact source commit `b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3`. The published `v1.0.0-beta.4` tag predates the Stable plugin manifest and `itambox.plugins.testing` helper, so CI uses this immutable commit until a release containing those interfaces is available. The pin is recorded in `.github/workflows/ci.yml`.

## Run the plugin verification tests

The tests use the host-provided `itambox.plugins.testing.verify_plugins` helper. The host application is not a pip-installable distribution; use a source checkout at the same immutable ref as CI and let `uv` install its locked dependencies. On Ubuntu, install the native LDAP build prerequisites first; CI does this automatically:

```sh
sudo apt-get update
sudo apt-get install --no-install-recommends -y build-essential libldap2-dev libsasl2-dev libssl-dev
```

The integration suite requires PostgreSQL 16. Set `ITAMBOX_DB_*` to a disposable test database, enable this plugin, and provide the required `display_label` value. Then run from the plugin repository root:

```sh
git clone https://github.com/itambox-community/itambox-webapp.git itambox-webapp
git -C itambox-webapp checkout b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3
uv sync --project itambox-webapp --locked --group dev
uv build
uv pip install --python itambox-webapp/.venv/bin/python dist/*.whl
ITAMBOX_ENV=dev ITAMBOX_PLUGINS=itambox_plugin_reference \
  ITAMBOX_PLUGINS_CONFIG='{"itambox_plugin_reference":{"display_label":"Plugin test"}}' \
  PYTHONPATH=itambox-webapp/itambox \
  uv run --project itambox-webapp --locked --no-sync \
  pytest -c itambox-webapp/pyproject.toml tests -q
uv run --project itambox-webapp --locked --no-sync \
  djlint src/itambox_plugin_reference/templates --check --lint
```

On Windows, pass `itambox-webapp/.venv/Scripts/python.exe` to `uv pip install`; use the host source directory in `PYTHONPATH` with the platform's path separator. The CI workflow is the canonical, Linux-tested version of these steps.

## Release process

1. Update the package version in `src/itambox_plugin_reference/__init__.py` and add a `CHANGELOG.md` entry.
2. Push a matching `vX.Y.Z` tag. The `Release` workflow builds a wheel and source distribution and attaches both to a GitHub Release. It does not publish to PyPI.
3. After reviewing the GitHub Release, a maintainer may run the `Publish to PyPI` workflow manually with that tag. It uses PyPI Trusted Publishing (OIDC); no API token is stored in this repository.

Before the first PyPI publication, a maintainer must create or claim the PyPI project `itambox-plugin-reference` and configure a Trusted Publisher with:

- Owner: `itambox-community`
- Repository: `itambox-plugin-reference`
- Workflow: `publish.yml`
- GitHub environment: `pypi`

The GitHub repository must have an environment named `pypi`. Configure required reviewers there if publication should require a second explicit approval. The workflow has only `id-token: write` for OIDC and `contents: read`; it does not need a PyPI token or other repository secret. No PyPI upload has been performed for this scaffold.
