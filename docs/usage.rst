Usage Guide
===========

Running the Server
------------------

The simplest way to run Mousetail is:

.. code-block:: bash

   uvx mousetail

This will start the MCP server using the latest version from PyPI.

Integrating with Claude
-----------------------

Claude Code (CLI)
~~~~~~~~~~~~~~~~~

1. **Add the MCP server with user scope (available globally):**

   .. code-block:: bash

      claude mcp add --transport stdio --scope user anki -- uvx mousetail

   **Flags explained:**

   - ``--transport stdio``: Specifies stdio communication
   - ``--scope user``: Makes the server available in all Claude Code sessions (not just current project)
   - ``anki``: The name you want to give this MCP server
   - ``--``: Separates Claude Code flags from the server command
   - ``uvx mousetail``: Runs the mousetail package from PyPI using uvx

2. **Verify it's configured:**

   .. code-block:: bash

      claude mcp list

3. **Start using it in any Claude Code session:**

   .. code-block:: text

      "List my Anki decks"
      "Create a flashcard in my Spanish deck"

That's it! Claude Code will now have access to your Anki collections across all sessions.

**Note:** If you prefer to use pip instead of uvx, you can install with ``pip install mousetail`` and then add the server with:

.. code-block:: bash

   claude mcp add --transport stdio --scope user anki -- python -m mousetail.mcp.stdio_server

Claude Desktop (GUI App)
~~~~~~~~~~~~~~~~~~~~~~~~~

For the Claude Desktop application:

1. **Edit your Claude Desktop configuration file:**

   - **macOS:** ``~/Library/Application Support/Claude/claude_desktop_config.json``
   - **Windows:** ``%APPDATA%\Claude\claude_desktop_config.json``
   - **Linux:** ``~/.config/Claude/claude_desktop_config.json``

2. **Add the MCP server configuration:**

   .. code-block:: json

      {
        "mcpServers": {
          "anki": {
            "command": "uvx",
            "args": ["mousetail"]
          }
        }
      }

3. **Restart Claude Desktop**

   Close and reopen Claude Desktop for the changes to take effect.

4. **Start Using!**

   You can now ask Claude to interact with your Anki:

   .. code-block:: text

      "List my Anki decks"
      "Create a flashcard in my Spanish deck with 'Hola' on the front and 'Hello' on the back"
      "Search for all cards in my Physics deck that are tagged 'formulas'"

Example Use Cases
-----------------

- Selectively commit what you learn in conversation with an LLM to memory.

  - *"Create an anki deck based on our conversation"*
  - *"Create a card in the algebra deck"*

- Use an LLM to interact with your deck.

  - *"Work through the algebra deck with me"*

Important Notes
---------------

Anki Must Be Closed
~~~~~~~~~~~~~~~~~~~

The MCP server and Anki application both access the same SQLite database files directly. Because SQLite uses file-based locking, **you should close Anki before using the MCP server**. Attempting to use both simultaneously can result in "Collection is locked" errors.

How Collections Are Accessed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MCP server finds Anki collections at their standard locations:

- **macOS:** ``~/Library/Application Support/Anki2/[Profile]/collection.anki2``
- **Linux:** ``~/.local/share/Anki2/[Profile]/collection.anki2``
- **Windows:** ``%APPDATA%\Anki2\[Profile]\collection.anki2``

You don't need to configure paths - the server automatically discovers available collections.

Configuration
-------------

Edit ``config.json`` to customize settings:

.. code-block:: json

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
