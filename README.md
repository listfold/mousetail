# The simplest and most stable Anki MCP Server.

Selectively commit what you learn in conversation with an LLM to memory using Anki - a flashcard learning system.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.21+-purple.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[API Documentation](https://listfold.github.io/mousetail/)** 

## Features
- Supports a minimal set of core anki operations, (CRUD & search flashcards and collections).
- Zero dependencies, works directly with anki's fairly stable pylib api.
- Doesn't require any addons, works with a basic anki installation.
- Good documentation.

## Installation

### Prerequisites

- Python 3.10 or higher
- [UV](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Anki 2.1.50+ installed.
- **Note:** Anki application should be closed when using the MCP server.

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

The MCP server and Anki application both access the same SQLite database files directly. Because SQLite uses file-based locking, **you must close Anki before using the MCP server**. Attempting to use both simultaneously will result in "Collection is locked" errors.

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
   ```bash
   open docs/_build/html/index.html  # macOS
   xdg-open docs/_build/html/index.html  # Linux
   start docs/_build/html/index.html  # Windows
   ```

The documentation is automatically built and deployed to GitHub Pages on every push to the main branch.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Anki](https://apps.ankiweb.net/) - The amazing spaced repetition software
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol by Anthropic
