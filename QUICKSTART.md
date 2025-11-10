# Quick Start Guide

Get up and running with Anki MCP Server in 2 minutes.

## Prerequisites

- Python 3.10+
- [UV package manager](https://github.com/astral-sh/uv)
- Anki installed (it creates the collections we'll access)

## Installation

```bash
# Clone the repository
git clone https://github.com/listfold/mousetail.git
cd mousetail

# Install dependencies
uv sync

# Test it works
uv run python test_server.py
```

You should see ✓ All tests passed!

## Setup for Claude Code (This CLI!)

**The easiest way** - use the `/mcp` command:

```
/mcp add anki
```

When prompted:
- **Command:** `uv run python -m mousetail.mcp.stdio_server`
- **Working directory:** `/Users/yourusername/Projects/mousetail` (use your actual path)

That's it! You can now use it:

```
"List my Anki decks"
"Create a new deck called 'Python Programming'"
"Add a flashcard to my Spanish deck: Front='Hola', Back='Hello'"
```

## Setup for Claude Desktop

1. **Edit configuration file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add this:**
   ```json
   {
     "mcpServers": {
       "anki": {
         "command": "uv",
         "args": ["run", "python", "-m", "mousetail.mcp.stdio_server"],
         "cwd": "/absolute/path/to/mousetail"
       }
     }
   }
   ```

3. **Restart Claude Desktop**

## Common Use Cases

### Create Flashcards

```
"Create a flashcard in my Japanese deck:
Front: 'ありがとう'
Back: 'Thank you'
Tags: greetings, basics"
```

### Search Your Cards

```
"Find all cards in my Physics deck that are tagged 'formulas'"
"Search for cards about Python in my programming deck"
```

### Manage Decks

```
"What decks do I have?"
"Create a new deck called 'Machine Learning'"
"Show me statistics for my Spanish deck"
```

### Bulk Operations

```
"Create 5 flashcards about common Spanish greetings"
"Find all cards I haven't reviewed in 30 days"
```

## Troubleshooting

### "No collections found"
- Make sure Anki has been run at least once
- This creates the default collection

### "Collection is locked"
- Close Anki if it's running
- Only one process can access a collection at a time

### "Command not found: uv"
- Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Or visit: https://github.com/astral-sh/uv

### Claude Code can't find the server
- Use absolute path in working directory
- Run `pwd` in the mousetail folder to get the full path

## What's Available?

### 9 MCP Tools:
1. `list_collections` - Find all your Anki collections
2. `get_collection_info` - Get stats (card count, etc.)
3. `list_decks` - See all your decks
4. `create_deck` - Make new decks
5. `list_note_types` - See available card templates
6. `create_note` - Add flashcards
7. `search_notes` - Find cards by query
8. `get_note` - Get note details
9. `update_note` - Modify existing cards

## Example Session

```
You: "What Anki decks do I have?"
Claude: I'll check your Anki decks...
        You have 3 decks:
        - Default (50 cards)
        - Spanish (120 cards)
        - Programming (85 cards)

You: "Create a flashcard in Spanish deck about 'gracias'"
Claude: I'll create that flashcard...
        ✓ Created flashcard in Spanish deck
        - Front: "gracias"
        - Back: "thank you"
        - Card ID: 1234567890

You: "Search for all cards tagged 'verbs' in my Spanish deck"
Claude: I'll search for those cards...
        Found 23 cards tagged 'verbs' in Spanish deck
```

## Next Steps

- Try creating flashcards with Claude!
- Use Anki search syntax for powerful queries
- Install as Anki addon (see main README)
- Customize config.json for your needs

## Need Help?

- Full documentation: See README.md
- Anki search syntax: https://docs.ankiweb.net/searching.html
- MCP documentation: https://modelcontextprotocol.io/

Happy studying! 📚✨
