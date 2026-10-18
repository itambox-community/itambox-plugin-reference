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

Plugin configuration is supplied through `ITAMBOX_PLUGINS_CONFIG`, keyed by the package name. The initial scaffold has no plugin-specific settings, so an empty object is sufficient:

```sh
ITAMBOX_PLUGINS_CONFIG='{"itambox_plugin_reference": {}}'
```

Do not put secrets in source control. Any secret configuration must be provided by the deployment's secret-management channel.

## Compatibility

The manifest declares one product compatibility range, `>=1.0,<1.1`. This accepts patch releases within 1.0 and intentionally does not declare a separate plugin API version. The plugin's own release version is independent of the product range.

The current CI host pin is the exact source commit `b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3`. The published `v1.0.0-beta.4` tag predates the Stable plugin manifest and `itambox.plugins.testing` helper, so CI uses this immutable commit until a release containing those interfaces is available. The pin is recorded in `.github/workflows/ci.yml`.

## Run the plugin verification tests

The tests use the host-provided `itambox.plugins.testing.verify_plugins` helper. The host application is not a pip-installable distribution; use a source checkout at the same immutable ref as CI and let `uv` install its locked dependencies:

```sh
git clone https://github.com/itambox-community/itambox-webapp.git itambox-webapp
git -C itambox-webapp checkout b82f4580e5cd9ad0ed0f28abb769d48d183bf1f3
uv sync --project itambox-webapp --locked --group dev
uv build
uv pip install --python itambox-webapp/.venv/bin/python dist/*.whl
PYTHONPATH=itambox-webapp/itambox uv run --project itambox-webapp --locked --no-sync python -m unittest discover -s tests -p 'test_*.py' -v
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
