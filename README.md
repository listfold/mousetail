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

For convenience the **[API Documentation](https://listfold.github.io/mousetail/)** includes instructions for integrating with Claude Code and Claude Desktop.

### Usecases
- Selectively commit what you learn in conversation with an LLM to memory.
  > "Create an anki deck based on our conversation"
  > "Create a card in the algebra deck"
- Use an LLM to interact with your deck.
  > "Work through the algebra deck with me"

## Features
- Minimal - supports core anki operations, create, read, update and delete.
- Stable - works directly with anki's stable pylib api, no addons or deps.

## Usage

### Claude Code (CLI)

1. **Add the MCP server with user scope (available globally):**
   ```bash
   claude mcp add --transport stdio --scope user anki -- uvx mousetail
   ```

   **Flags explained:**
   - `--transport stdio`: Specifies stdio communication
   - `--scope user`: Makes the server available in all Claude Code sessions (not just current project)
   - `anki`: The name you want to give this MCP server
   - `--`: Separates Claude Code flags from the server command
   - `uvx mousetail`: Runs the mousetail package from PyPI using uvx

2. **Verify it's configured:**
   ```bash
   claude mcp list
   ```

3. **Start using it in any Claude Code session:**
   ```
   "List my Anki decks"
   "Create a flashcard in my Spanish deck"
   ```

That's it! Claude Code will now have access to your Anki collections across all sessions.

**Note:** If you prefer to use pip instead of uvx, you can install with `pip install mousetail` and then add the server with:
```bash
claude mcp add --transport stdio --scope user anki -- python -m mousetail.mcp.stdio_server
```

### Claude Desktop (GUI App)

For the Claude Desktop application:

1. **Edit your Claude Desktop configuration file:**

   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Add the MCP server configuration:**

   ```json
   {
     "mcpServers": {
       "anki": {
         "command": "uvx",
         "args": ["mousetail"]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

   Close and reopen Claude Desktop for the changes to take effect.

4. **Start Using!**

   You can now ask Claude to interact with your Anki:

   ```
   "List my Anki decks"
   "Create a flashcard in my Spanish deck with 'Hola' on the front and 'Hello' on the back"
   "Search for all cards in my Physics deck that are tagged 'formulas'"
   ```

## Important Notes

### Anki Must Be Closed

The MCP server and Anki application both access the same SQLite database files directly. Because SQLite uses file-based locking, **you should close Anki before using the MCP server**. Attempting to use both simultaneously can result in "Collection is locked" errors.

### How Collections Are Accessed

The MCP server finds Anki collections at their standard locations:
- **macOS:** `~/Library/Application Support/Anki2/[Profile]/collection.anki2`
- **Linux:** `~/.local/share/Anki2/[Profile]/collection.anki2`
- **Windows:** `%APPDATA%\Anki2\[Profile]\collection.anki2`

You don't need to configure paths - the server automatically discovers available collections.

## Configuration

Edit `config.json` to customize settings:

```json
{
  "collection": {
    "auto_open_default": true,
    "default_path": null
  },
  "logging": {
    "level": "INFO",
    "file": null
  }
}
```

## Development

### Core goals

Mousetail was written because all the existing MCP Anki tools depend on the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) addon.

AnkiConnect is a HTTP server for Anki, it was originally created to support connecting browser extensions like [yomichan](https://ankiweb.net/shared/info/934748696) to Anki. For MCP development it is not necessary and introduces issues:
- introduces complexity (for example a dedicated HTTP server for Anki occupies a port)
- introduces risk - if the AnkiConnect API changes or has a bug the MCP tool will break
- introduces an extra step - all current MCP tools require installing the AnkiConnect addon

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

## Acknowledgments

- [Anki](https://apps.ankiweb.net/) - The amazing spaced repetition software
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol by Anthropic
