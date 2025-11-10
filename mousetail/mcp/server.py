"""MCP Server implementation for Anki.

This module provides the main MCP (Model Context Protocol) server implementation
that exposes Anki functionality to LLMs like Claude. It handles tool registration,
request routing, and response formatting.
"""

import logging
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from mousetail.server.collection_manager import get_manager
from mousetail.mcp.tools import (
    list_collections_tool,
    list_decks_tool,
    list_note_types_tool,
    create_note_tool,
    search_notes_tool,
    get_note_tool,
    update_note_tool,
    create_deck_tool,
    get_collection_info_tool,
)


logger = logging.getLogger(__name__)


class AnkiMCPServer:
    """MCP Server for Anki operations.

    This class implements the Model Context Protocol server that provides
    LLMs with access to Anki collections. It manages tool definitions,
    handles incoming requests, and coordinates with the CollectionManager
    to perform operations on Anki databases.

    Attributes:
        server: The underlying MCP Server instance.
        manager: CollectionManager instance for database operations.

    Example:
        >>> server = AnkiMCPServer()
        >>> mcp_server = server.get_server()
    """

    def __init__(self):
        """Initialize the Anki MCP server.

        Creates a new MCP server instance named "anki-mcp" and sets up
        all tool handlers for Anki operations.
        """
        self.server = Server("anki-mcp")
        self.manager = get_manager()
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP server handlers.

        Registers the list_tools and call_tool handlers with the MCP server.
        These handlers define the available operations and route requests
        to the appropriate tool implementations.
        """

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools.

            Returns:
                List of Tool objects describing available Anki operations.
            """
            return [
                Tool(
                    name="list_collections",
                    description="List all available Anki collections on the system",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_collection_info",
                    description="Get information about an Anki collection (name, card count, note count)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "collection_path": {
                                "type": "string",
                                "description": "Path to collection file (optional, uses default if not provided)"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="list_decks",
                    description="List all decks in the collection with their names and IDs",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "collection_path": {
                                "type": "string",
                                "description": "Path to collection file (optional)"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="create_deck",
                    description="Create a new deck in the collection",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "deck_name": {
                                "type": "string",
                                "description": "Name of the deck to create"
                            },
                            "collection_path": {
                                "type": "string",
                                "description": "Path to collection file (optional)"
                            }
                        },
                        "required": ["deck_name"]
                    }
                ),
                Tool(
                    name="list_note_types",
                    description="List all note types (card templates) available in the collection",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "collection_path": {
                                "type": "string",
                                "description": "Path to collection file (optional)"
                            }
                        },
                        "required": []
                    }
                ),
                Tool(
                    name="create_note",
                    description="Create a new note (flashcard) in Anki. A note generates one or more cards based on the note type template.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "deck_name": {
                                "type": "string",
                                "description": "Name of the deck where the note should be added"
                            },
                            "note_type_name": {
                                "type": "string",
                                "description": "Name of the note type (e.g., 'Basic', 'Cloze')"
                            },
                            "fields": {
                                "type": "object",
                                "description": "Field name to value mapping (e.g., {'Front': 'Question', 'Back': 'Answer'})",
                                "additionalProperties": {"type": "string"}
                            },
                            "tags": {
                                "type": "array",
                                "description": "Optional list of tags",
                                "items": {"type": "string"},
                                "default": []
                            },
                            "collection_path": {
                                "type": "string",
                                "description": "Path to collection file (optional)"
                            }
                        },
                        "required": ["deck_name", "note_type_name", "fields"]
                    }
                ),
                Tool(
                    name="search_notes",
                    description="Search for notes using Anki search syntax. Examples: 'deck:MyDeck', 'tag:important', 'front:*python*'",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Anki search query"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results (optional)",
                                "default": 100
                            },
                            "collection_path": {
                                "type": "string",
                                "description": "Path to collection file (optional)"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_note",
                    description="Get detailed information about a specific note by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "note_id": {
                                "type": "integer",
                                "description": "ID of the note to retrieve"
                            },
                            "collection_path": {
                                "type": "string",
                                "description": "Path to collection file (optional)"
                            }
                        },
                        "required": ["note_id"]
                    }
                ),
                Tool(
                    name="update_note",
                    description="Update an existing note's fields and/or tags",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "note_id": {
                                "type": "integer",
                                "description": "ID of the note to update"
                            },
                            "fields": {
                                "type": "object",
                                "description": "Field name to value mapping for fields to update",
                                "additionalProperties": {"type": "string"}
                            },
                            "tags": {
                                "type": "array",
                                "description": "New list of tags (replaces existing tags)",
                                "items": {"type": "string"}
                            },
                            "collection_path": {
                                "type": "string",
                                "description": "Path to collection file (optional)"
                            }
                        },
                        "required": ["note_id"]
                    }
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """Handle tool calls.

            Routes incoming tool requests to the appropriate implementation
            and returns formatted results.

            Args:
                name: Name of the tool to execute.
                arguments: Dictionary of arguments for the tool.

            Returns:
                List containing a TextContent object with the result.
            """
            try:
                logger.info(f"Tool called: {name} with args: {arguments}")

                if name == "list_collections":
                    result = await list_collections_tool()
                elif name == "get_collection_info":
                    result = await get_collection_info_tool(
                        arguments.get("collection_path")
                    )
                elif name == "list_decks":
                    result = await list_decks_tool(
                        arguments.get("collection_path")
                    )
                elif name == "create_deck":
                    result = await create_deck_tool(
                        arguments["deck_name"],
                        arguments.get("collection_path")
                    )
                elif name == "list_note_types":
                    result = await list_note_types_tool(
                        arguments.get("collection_path")
                    )
                elif name == "create_note":
                    result = await create_note_tool(
                        arguments["deck_name"],
                        arguments["note_type_name"],
                        arguments["fields"],
                        arguments.get("tags", []),
                        arguments.get("collection_path")
                    )
                elif name == "search_notes":
                    result = await search_notes_tool(
                        arguments["query"],
                        arguments.get("limit", 100),
                        arguments.get("collection_path")
                    )
                elif name == "get_note":
                    result = await get_note_tool(
                        arguments["note_id"],
                        arguments.get("collection_path")
                    )
                elif name == "update_note":
                    result = await update_note_tool(
                        arguments["note_id"],
                        arguments.get("fields"),
                        arguments.get("tags"),
                        arguments.get("collection_path")
                    )
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return [TextContent(
                    type="text",
                    text=str(result)
                )]
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

    def get_server(self) -> Server:
        """Get the MCP server instance.

        Returns:
            The configured MCP Server instance ready for use.
        """
        return self.server
