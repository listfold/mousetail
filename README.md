# Anki MCP Server

Selectively commit what you learn in conversation with an LLM to memory using a rigorous and proven learning framework.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.21+-purple.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A standalone MCP (Model Context Protocol) server that enables LLMs like Claude to interact with your Anki flashcard collections using Anki's Python library (pylib).

📚 **[View Full Documentation](https://listfold.github.io/ankimcp/)** - Interactive tool reference with all MCP tools and parameters

## How It Works

This MCP server uses Anki's `pylib` (Python library) to directly access your Anki collection files (SQLite databases). It operates **independently of the Anki application** - in fact, Anki must be closed when using the MCP server to avoid database locking conflicts.

## Goal
This is a tool that routes what you learn in conversation with an LLM to a robust and rigorous learning framework (anki).

## Features
- Supports a minimal set of core anki operations, (CRUD & search flashcards and collections)
- Zero dependencies, works directly with anki's fairly stable pylib.
- Stdio transport, no need to manage HTTP ports etc...
- Threadsafe access to anki collections.
- Good documentation

## Installation

### Prerequisites

- Python 3.10 or higher
- [UV](https://github.com/astral-sh/uv) package manager
- Anki 2.1.50+ installed (to create collections)
- **Note:** Anki application must be closed when using the MCP server

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/listfold/ankimcp.git
cd ankimcp
```

2. **Install dependencies:**
```bash
uv sync
```

3. **Test the installation:**
```bash
uv run python test_server.py
```

## Usage

### Option 1: Claude Code (CLI)

Claude Code is the CLI tool you're using right now. To add this MCP server:

1. **Use the `/mcp` command:**
```
/mcp add anki
```

2. **When prompted, provide the command:**
```
uv run python -m ankimcp.mcp.stdio_server
```

3. **When prompted for the working directory:**
```
/Users/yourusername/Projects/ankimcp
```
(Use the absolute path to this directory)

4. **Start using it immediately:**
```
"List my Anki decks"
"Create a flashcard in my Spanish deck"
```

That's it! Claude Code will now have access to your Anki collections.

### Option 2: Claude Desktop (GUI App)

For the Claude Desktop application:

1. **Configure Claude Desktop**

   Edit your Claude Desktop configuration file:
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Add the MCP server configuration:**

   ```json
   {
     "mcpServers": {
       "anki": {
         "command": "uv",
         "args": [
           "run",
           "python",
           "-m",
           "ankimcp.mcp.stdio_server"
         ],
         "cwd": "/absolute/path/to/ankimcp"
       }
     }
   }
   ```

   Replace `/absolute/path/to/ankimcp` with the actual path to this directory.

3. **Restart Claude Desktop**

   Close and reopen Claude Desktop for the changes to take effect.

4. **Start Using!**

   You can now ask Claude to interact with your Anki:

   ```
   "List my Anki decks"
   "Create a flashcard in my Spanish deck with 'Hola' on the front and 'Hello' on the back"
   "Search for all cards in my Physics deck that are tagged 'formulas'"
   ```

## MCP Tools

The following tools are available when using Claude Desktop:

### `list_collections`
List all available Anki collections on your system.

### `get_collection_info`
Get information about a collection (name, card count, note count).
- **Parameters:** `collection_path` (optional)

### `list_decks`
List all decks in the collection.
- **Parameters:** `collection_path` (optional)

### `create_deck`
Create a new deck.
- **Parameters:** `deck_name` (required), `collection_path` (optional)

### `list_note_types`
List all note types with their fields.
- **Parameters:** `collection_path` (optional)

### `create_note`
Create a new flashcard note.
- **Parameters:**
  - `deck_name` (required): Target deck
  - `note_type_name` (required): Note type (e.g., "Basic", "Cloze")
  - `fields` (required): Field name to value mapping
  - `tags` (optional): Array of tags
  - `collection_path` (optional)

**Example:**
```json
{
  "deck_name": "Japanese",
  "note_type_name": "Basic",
  "fields": {
    "Front": "こんにちは",
    "Back": "Hello"
  },
  "tags": ["vocabulary", "greetings"]
}
```

### `search_notes`
Search for notes using Anki's search syntax.
- **Parameters:** `query` (required), `limit` (optional), `collection_path` (optional)

**Query Examples:**
- `"deck:Japanese"` - Notes in Japanese deck
- `"tag:vocabulary"` - Notes with vocabulary tag
- `"front:*python*"` - Notes with "python" in front field

### `get_note`
Get detailed information about a specific note.
- **Parameters:** `note_id` (required), `collection_path` (optional)

### `update_note`
Update an existing note's fields and/or tags.
- **Parameters:** `note_id` (required), `fields` (optional), `tags` (optional), `collection_path` (optional)

## Important Notes

### Anki Must Be Closed

The MCP server and Anki application both access the same SQLite database files directly. Because SQLite uses file-based locking, **you must close Anki before using the MCP server**. Attempting to use both simultaneously will result in "Collection is locked" errors.

### How Collections Are Accessed

The MCP server finds Anki collections at their standard locations:
- **macOS:** `~/Library/Application Support/Anki2/[Profile]/collection.anki2`
- **Linux:** `~/.local/share/Anki2/[Profile]/collection.anki2`
- **Windows:** `%APPDATA%\Anki2\[Profile]\collection.anki2`

You don't need to configure paths - the server automatically discovers available collections.

## Project Structure

```
ankimcp/
├── config.json              # Server configuration
├── ankimcp/
│   ├── server/
│   │   └── collection_manager.py  # Collection lifecycle management
│   └── mcp/
│       ├── server.py        # MCP server implementation
│       ├── tools.py         # MCP tool implementations
│       └── stdio_server.py  # stdio transport entry point
└── test_server.py          # Test script
```

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

### Running Tests

```bash
uv run python test_server.py
```

### Manual Testing

```bash
# Start the MCP server (for testing)
uv run python -m ankimcp.mcp.stdio_server
```

The server communicates via stdin/stdout using the MCP protocol.


## Architecture

```
Claude Desktop / Claude Code / MCP Client
        ↓ stdio (JSON-RPC)
    MCP Server (this project)
        ↓ Python API calls
   Collection Manager (thread-safe wrapper)
        ↓ Direct library calls
    Anki pylib (Anki's Python library)
        ↓ Rust backend
   SQLite Database (collection.anki2 files)
```

**Key Points:**
- The MCP server is a standalone Python application
- Uses Anki's `pylib` - the same library Anki desktop uses internally
- No network communication - direct SQLite file access
- Anki application does NOT need to be running (in fact, it must be closed)
- No dependencies beyond `anki` and `mcp` Python packages

## Troubleshooting

### Collection Access Issues

**Error: "No default collection found"**
- Ensure Anki has been run at least once
- Or specify `collection_path` in tool calls

**Error: "Collection is locked"**
- Close Anki if it's running
- Only one process can access a collection at a time

### Claude Desktop Integration

**MCP server not showing in Claude**
- Verify the path in `claude_desktop_config.json` is correct (absolute path)
- Check Claude Desktop logs for errors
- Restart Claude Desktop after configuration changes

**Test the configuration:**
```bash
# Verify UV is in PATH
which uv

# Test the server starts
uv run python -m ankimcp.mcp.stdio_server
# (Press Ctrl+C to stop)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Anki](https://apps.ankiweb.net/) - The amazing spaced repetition software
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol by Anthropic
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager

## Support

For issues or questions:
- Open an issue on GitHub
- Check [Anki addon documentation](https://addon-docs.ankiweb.net/)
- Review [MCP documentation](https://modelcontextprotocol.io/)
