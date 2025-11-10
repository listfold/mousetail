AnkiMCP Documentation
=====================

AnkiMCP is a standalone MCP (Model Context Protocol) server that enables LLMs like Claude to interact with Anki flashcard collections using Anki's Python library.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api/index

Overview
--------

AnkiMCP provides a bridge between Large Language Models and Anki, allowing AI assistants to:

- Browse and manage Anki collections
- Create and modify decks
- Add, search, and update flashcards
- Query note types and collection information

The server implements the Model Context Protocol (MCP), making it compatible with Claude Desktop and other MCP-enabled applications.

Features
--------

- **Collection Management**: List and access multiple Anki profiles
- **Deck Operations**: Create decks and list existing ones
- **Note Management**: Create, search, update, and retrieve notes
- **Note Type Support**: Work with any Anki note type (Basic, Cloze, custom templates)
- **Search**: Full support for Anki's powerful search syntax
- **Thread-Safe**: Manages concurrent access to Anki databases

Installation
------------

Install using pip or uv:

.. code-block:: bash

   pip install ankimcp
   # or
   uv pip install ankimcp

Quick Start
-----------

Configure Claude Desktop to use AnkiMCP by adding to your config:

.. code-block:: json

   {
     "mcpServers": {
       "anki": {
         "command": "ankimcp"
       }
     }
   }

Then restart Claude Desktop. You can now ask Claude to interact with your Anki collections!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
