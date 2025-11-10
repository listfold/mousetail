Quick Start Guide
=================

This guide will help you get started with AnkiMCP.

Installation
------------

Install AnkiMCP using pip or uv:

.. code-block:: bash

   pip install ankimcp
   # or
   uv pip install ankimcp

Configuration
-------------

Claude Desktop
~~~~~~~~~~~~~~

Add AnkiMCP to your Claude Desktop configuration file:

**macOS**: ``~/Library/Application Support/Claude/claude_desktop_config.json``

**Windows**: ``%APPDATA%\Claude\claude_desktop_config.json``

Configuration:

.. code-block:: json

   {
     "mcpServers": {
       "anki": {
         "command": "ankimcp"
       }
     }
   }

If you want to specify a custom collection path:

.. code-block:: json

   {
     "mcpServers": {
       "anki": {
         "command": "ankimcp",
         "env": {
           "ANKI_COLLECTION_PATH": "/path/to/your/collection.anki2"
         }
       }
     }
   }

Restart Claude Desktop after making configuration changes.

Testing the Server
------------------

You can test the server directly from the command line:

.. code-block:: bash

   python -m ankimcp.mcp.stdio_server

This will start the server in stdio mode, which you can interact with using the MCP protocol.

Usage Examples
--------------

Once configured with Claude Desktop, you can ask Claude to:

List Collections
~~~~~~~~~~~~~~~~

.. code-block:: text

   Can you list all my Anki collections?

Create a Deck
~~~~~~~~~~~~~

.. code-block:: text

   Create a new deck called "Spanish Vocabulary"

Add Flashcards
~~~~~~~~~~~~~~

.. code-block:: text

   Add a flashcard to my Spanish Vocabulary deck:
   Front: "Hola"
   Back: "Hello"

Search Notes
~~~~~~~~~~~~

.. code-block:: text

   Search for all cards in my Spanish deck that contain "Hola"

Update a Note
~~~~~~~~~~~~~

.. code-block:: text

   Update note #12345 to add the tag "important"

Troubleshooting
---------------

Collection Not Found
~~~~~~~~~~~~~~~~~~~~

If you get "No default collection found", either:

1. Make sure Anki is installed and you've created at least one profile
2. Specify the collection path explicitly in the configuration
3. Check that the collection file exists at the expected location

Permission Errors
~~~~~~~~~~~~~~~~~

If you get permission errors:

1. Make sure Anki is not running (Anki locks the database when open)
2. Check file permissions on your collection file
3. Try specifying the collection path explicitly

Next Steps
----------

- Explore the :doc:`api/index` to understand available functions
- Check the `GitHub repository <https://github.com/listfold/ankimcp>`_ for more examples
