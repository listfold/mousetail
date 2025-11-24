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
 
> "Create a deck based on our conversation so I don't forget critical details"

Use an LLM to interact with your deck

> "Create a card - what is a coeffcient?, create a card - id the first coefficient in this polynomial"

Use an LLM to cleanup a deck
> "Check my french vocab deck for correctness and correct any mistakes, typos or errors"

## Syncing

Mousetail supports synchronizing your Anki collection with AnkiWeb or a self-hosted sync server. This allows you to keep your collection in sync across devices.

### Quick Start

Sync with AnkiWeb (saves credentials for future syncs):
```
> "Save my AnkiWeb credentials: username is myuser@example.com and password is mypassword"
> "Sync my collection with AnkiWeb"
```

### Credential Management

Mousetail stores credentials securely in your system's credential manager:
- **macOS:** Keychain
- **Windows:** Credential Manager
- **Linux:** Secret Service (GNOME Keyring, KWallet, etc.)

Available credential tools:
- `save_sync_credentials` - Save username/password securely
- `load_sync_credentials` - Load saved credentials
- `delete_sync_credentials` - Remove saved credentials

### Sync Options

The `sync_collection` tool supports:
- **AnkiWeb sync** (default) - Leave endpoint empty
- **Self-hosted servers** - Provide custom endpoint URL (e.g., `https://sync.example.com`)
- **Media sync** - Enabled by default, includes images and audio files
- **Collection-only sync** - Set `sync_media: false` to skip media

### Examples

**First-time setup with AnkiWeb:**
```
> "Save my sync credentials for AnkiWeb - username: user@example.com, password: mypass123"
> "Sync my collection"
```

**Using a self-hosted server:**
```
> "Save my sync credentials - username: john, password: secret, endpoint: https://sync.myserver.com"
> "Sync my collection"
```

**One-time sync without saving credentials:**
```
> "Sync my collection with AnkiWeb using username user@example.com and password mypass123"
```

**Collection-only sync (skip media):**
```
> "Sync my collection but don't sync media files"
```

### Configuration

You can set a default sync endpoint in `config.json`:
```json
{
  "sync": {
    "endpoint": "https://sync.example.com"
  }
}
```

Leave `endpoint` as `null` to use AnkiWeb by default.

### Important Notes

- **Close Anki first:** Sync will fail if the Anki application is running
- **Media sync:** Media sync is slower and uses more bandwidth but ensures images/audio are synced
- **Conflicts:** If conflicts occur, try syncing from Anki desktop first to resolve them
- **Security:** Credentials are never stored in plain text - they're kept in your system's secure credential storage

### Self-Hosted Sync Server Setup

To sync with your own server:
1. Set up an [Anki sync server](https://docs.ankiweb.net/sync-server.html)
2. Configure credentials on the server (using environment variables like `SYNC_USER1=user:password`)
3. Save your credentials in Mousetail with the server endpoint
4. Sync normally

For detailed sync server setup, see the [official Anki documentation](https://docs.ankiweb.net/sync-server.html).

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

### Local Development Setup

To develop and test Mousetail locally with Claude Code:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/listfold/mousetail.git
   cd mousetail
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure Claude Code:**
   The project includes a `.mcp.json` file that configures the MCP server for local development:
   ```json
   {
     "mcpServers": {
       "mousetail": {
         "type": "stdio",
         "command": "uv",
         "args": ["run", "python", "-m", "mousetail.mcp.stdio_server"],
         "env": {
           "PYTHONUNBUFFERED": "1"
         }
       }
     }
   }
   ```

4. **Restart Claude Code:**
   After the configuration is in place, restart Claude Code to load the MCP server.

5. **Verify the server:**
   - Use `/context` in Claude Code to see available MCP tools
   - The mousetail server should appear with all available tools (list_collections, create_note, sync_collection, etc.)

6. **Testing sync functionality:**
   - Close the Anki desktop application before testing
   - Test credential management: `save_sync_credentials`, `load_sync_credentials`, `delete_sync_credentials`
   - Test sync: `sync_collection` with your AnkiWeb credentials or self-hosted server

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
