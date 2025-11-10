# Documentation Setup

This document describes the Sphinx documentation setup for Mousetail.

## What's Been Set Up

### 1. Sphinx Configuration
- **Location**: `docs/conf.py`
- **Theme**: Furo (modern, clean theme)
- **Extensions**:
  - `sphinx.ext.autodoc` - Automatic API documentation from docstrings
  - `sphinx.ext.napoleon` - Support for Google/NumPy style docstrings
  - `sphinx.ext.viewcode` - Links to source code
  - `sphinx.ext.intersphinx` - Links to other project docs (e.g., Python)
  - `sphinx_autodoc_typehints` - Type hints in documentation

### 2. Documentation Structure

```
docs/
├── conf.py                      # Sphinx configuration
├── index.rst                    # Main documentation page
├── quickstart.rst               # Quick start guide
├── api/
│   ├── index.rst               # API overview
│   ├── server.rst              # AnkiMCPServer docs
│   ├── tools.rst               # Tool functions docs
│   └── collection_manager.rst  # CollectionManager docs
├── _static/                    # Static files (empty for now)
└── _build/                     # Generated HTML (gitignored)
```

### 3. Enhanced Docstrings

All Python modules now have comprehensive docstrings following Google style:
- `mousetail/mcp/server.py` - MCP server implementation
- `mousetail/mcp/tools.py` - Tool implementations
- `mousetail/server/collection_manager.py` - Collection management

Each function includes:
- Summary description
- Args section with type hints
- Returns section describing output
- Example usage where appropriate

### 4. GitHub Actions

Updated `.github/workflows/docs.yml` to:
1. Install documentation dependencies
2. Build Sphinx documentation
3. Deploy to GitHub Pages automatically on push to main

### 5. Dependencies

Added to `pyproject.toml`:
```toml
[project.optional-dependencies]
docs = [
    "sphinx>=7.0.0",
    "furo>=2024.0.0",
    "sphinx-autodoc-typehints>=2.0.0",
]
```

## Building Documentation Locally

### Install Dependencies
```bash
uv pip install ".[docs]"
```

### Build HTML
```bash
uv run python -m sphinx -b html docs docs/_build/html
```

### View Documentation
```bash
# macOS
open docs/_build/html/index.html

# Linux
xdg-open docs/_build/html/index.html

# Windows
start docs/_build/html/index.html
```

## Maintenance

### Adding New Modules

When adding new Python modules:

1. Add comprehensive docstrings to the module and all public functions/classes
2. Create a new `.rst` file in `docs/api/` (e.g., `docs/api/new_module.rst`)
3. Add automodule directives:
   ```rst
   New Module
   ==========

   .. automodule:: mousetail.new_module
      :members:
      :undoc-members:
      :show-inheritance:
   ```
4. Add the new file to the toctree in `docs/api/index.rst`

### Docstring Format

Use Google-style docstrings:

```python
def example_function(arg1: str, arg2: int = 10) -> dict:
    """Brief description of the function.

    More detailed explanation if needed. This can span
    multiple lines and include additional context.

    Args:
        arg1: Description of arg1.
        arg2: Description of arg2. Default is 10.

    Returns:
        Dict with 'key1' (str) and 'key2' (int).

    Raises:
        ValueError: If arg1 is empty.
        KeyError: If required key is missing.

    Example:
        >>> result = example_function("test", 20)
        >>> print(result['key1'])
        'test'
    """
    pass
```

### Updating Quick Start

Edit `docs/quickstart.rst` to update:
- Installation instructions
- Configuration examples
- Usage examples
- Troubleshooting tips

## Theme Customization

The Furo theme can be customized in `docs/conf.py`:

```python
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    # Add more options as needed
}
```

See [Furo documentation](https://pradyunsg.me/furo/) for all available options.

## Deployment

Documentation is automatically deployed via GitHub Actions:
1. Push to main branch triggers the workflow
2. Workflow builds Sphinx docs
3. Generated HTML is deployed to GitHub Pages
4. Accessible at: https://listfold.github.io/mousetail/

## Troubleshooting

### Duplicate Object Warnings

The warnings about "duplicate object description" are normal and occur when using both:
- `.. automodule::` (includes all members)
- Explicit `.. autofunction::` or `.. autoclass::` directives

These warnings don't affect the output. To suppress them, add `:no-index:` to the explicit directives.

### Import Errors

If Sphinx can't import modules:
1. Ensure all dependencies are installed: `uv pip install ".[docs]"`
2. Check that `sys.path.insert(0, os.path.abspath('..'))` is in `conf.py`
3. Verify the package structure has proper `__init__.py` files

### Build Fails in CI

If GitHub Actions fails:
1. Check the workflow logs for specific errors
2. Test the build locally first
3. Ensure all doc dependencies are in `pyproject.toml`
4. Verify Python version matches between local and CI (3.10)
