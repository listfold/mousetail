<div align="center">
  <img src="https://github.com/listfold/mousetail/blob/main/mousetail_transparent.png?raw=true" alt="Mousetail Logo" width="200"/>
</div>

# The simplest and most stable MCP Server for Anki

[![UV](https://img.shields.io/badge/Package%20Manager-UV-blueviolet)](https://docs.astral.sh/uv/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.21+-purple.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Mousetail's goal is to be the simplest and most reliable way of connecting Anki to an LLM. It does not require any addons, just have anki installed and an LLM you'd like to connect to your decks.

Running the server is as simple as:

```bash
uvx mousetail
```

For detailed instructions on integrating with Claude Code, Claude Desktop, and other LLM tools:

**[Usage Guide](https://listfold.github.io/mousetail/usage.html)**

**[API Reference](https://listfold.github.io/mousetail/api/index.html)**

## Features
- **Minimal** - supports core anki operations: create, read, update and delete
- **Stable** - works directly with anki's stable pylib api, no addons or deps
- **Simple** - no configuration required, automatically discovers your Anki collections

## Use Cases

Selectively commit what you learn in conversation with an LLM to memory
 
> "Create a deck based on our conversation"

Use an LLM to interact with your deck

> "Work through the algebra deck with me"

Prompt an LLM to periodically quiz you.

> "Every 10 prompts, ignore my prompts until i have worked through 5 cards"

## Important Notes

### How Collections Are Accessed

The MCP server finds Anki collections at their standard locations:
- **macOS:** `~/Library/Application Support/Anki2/[Profile]/collection.anki2`
- **Linux:** `~/.local/share/Anki2/[Profile]/collection.anki2`
- **Windows:** `%APPDATA%\Anki2\[Profile]\collection.anki2`

You don't need to configure paths - the server automatically discovers available collections, this can be customized using configuration.

## Configuration

The server can be customized through a `config.json` file. See the **[Usage Guide](https://listfold.github.io/mousetail/usage.html)** for configuration options.

## Development

### Core goals

Mousetail was written because all the existing MCP Anki tools depend on the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) addon.

AnkiConnect is a HTTP server for Anki, it was originally created to support connecting browser extensions like [yomichan](https://ankiweb.net/shared/info/934748696) to Anki. For MCP development, it is not necessary and introduces issues:
- introduces complexity e.g. a dedicated HTTP server for Anki occupies a port
- introduces risk e.g. if the AnkiConnect API changes or has a bug the MCP tool will break
- introduces an extra step e.g. all current MCP tools require installing the AnkiConnect addon

Mousetail has a much simpler approach. It integrates directly with Anki's [pylib](https://addon-docs.ankiweb.net/the-anki-module.html). This is a stable API that's part of Anki's core, it therefore is not subject to arbitrary or frequent change, and does not require any 3rd-party addons.

Because it prioritizes simplicity, mousetail will remain more stable than the alternatives. The tradeoff is that Mousetail will never integrate with the Anki UI. It is also reasonable to assume that Mousetail will only ever work with colocated (same system) LLM tools and Anki decks.

### Building Documentation

The project uses Sphinx with the Furo theme to generate documentation from Python docstrings.

1. **Install documentation dependencies:**
   ```bash
   uv pip install ".[docs]"
   ```

2. **Build the documentation:**
   ```bash
   uv run python -m sphinx -b html docs docs/_build/html
   ```

3. **View the documentation:**
   Open `docs/_build/html/index.html` in your browser.

The documentation is automatically built and deployed to GitHub Pages on every push to the main branch.

## License

MIT License - see LICENSE file for details.
