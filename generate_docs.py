#!/usr/bin/env python3
"""Generate MCP server documentation from tool definitions."""

import json


def main():
    """Extract tool definitions and generate documentation."""
    # Tool definitions from mousetail/mcp/server.py
    tools_data = [
        {
            "name": "list_collections",
            "description": "List all available Anki collections on the system",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "get_collection_info",
            "description": "Get information about an Anki collection (name, card count, note count)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "collection_path": {
                        "type": "string",
                        "description": "Path to collection file (optional, uses default if not provided)"
                    }
                },
                "required": []
            }
        },
        {
            "name": "list_decks",
            "description": "List all decks in the collection with their names and IDs",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "collection_path": {
                        "type": "string",
                        "description": "Path to collection file (optional)"
                    }
                },
                "required": []
            }
        },
        {
            "name": "create_deck",
            "description": "Create a new deck in the collection",
            "inputSchema": {
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
        },
        {
            "name": "list_note_types",
            "description": "List all note types (card templates) available in the collection",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "collection_path": {
                        "type": "string",
                        "description": "Path to collection file (optional)"
                    }
                },
                "required": []
            }
        },
        {
            "name": "create_note",
            "description": "Create a new note (flashcard) in Anki. A note generates one or more cards based on the note type template.",
            "inputSchema": {
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
        },
        {
            "name": "search_notes",
            "description": "Search for notes using Anki search syntax. Examples: 'deck:MyDeck', 'tag:important', 'front:*python*'",
            "inputSchema": {
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
        },
        {
            "name": "get_note",
            "description": "Get detailed information about a specific note by ID",
            "inputSchema": {
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
        },
        {
            "name": "update_note",
            "description": "Update an existing note's fields and/or tags",
            "inputSchema": {
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
        }
    ]

    # Save to JSON file
    output_file = "docs/tools.json"
    with open(output_file, 'w') as f:
        json.dump({
            "server": "anki-mcp",
            "version": "0.1.0",
            "tools": tools_data
        }, f, indent=2)

    print(f"Generated {output_file} with {len(tools_data)} tools")


if __name__ == "__main__":
    main()
