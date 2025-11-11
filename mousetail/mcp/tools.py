"""Tool implementations for MCP server.

This module contains the actual implementation of each MCP tool exposed
by the Anki MCP server. Each function corresponds to a tool that LLMs
can call to interact with Anki collections.
"""

import json
from typing import Optional
from mousetail.server.collection_manager import get_manager


async def list_collections_tool() -> dict:
    """List all available Anki collections.

    Scans the system for Anki profile directories and returns information
    about all discovered collections.

    Returns:
        Dict with 'collections' (list of collection info) and 'count' (int).
    """
    manager = get_manager()
    collections = manager.list_available_collections()
    return {
        "collections": collections,
        "count": len(collections)
    }


async def get_collection_info_tool(collection_path: Optional[str] = None) -> dict:
    """Get information about a collection.

    Args:
        collection_path: Path to the collection file. If None, uses the default collection.

    Returns:
        Dict with 'success' (bool), 'collection' (info dict) or 'error' (str).
    """
    manager = get_manager()
    try:
        info = manager.get_collection_info(collection_path)
        return {
            "success": True,
            "collection": info
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def list_decks_tool(collection_path: Optional[str] = None) -> dict:
    """List all decks in the collection.

    Args:
        collection_path: Path to the collection file. If None, uses the default collection.

    Returns:
        Dict with 'success' (bool), 'decks' (list), 'count' (int) or 'error' (str).
    """
    manager = get_manager()
    try:
        with manager.get_collection(collection_path) as col:
            decks = []
            for deck_name_id in col.decks.all_names_and_ids():
                decks.append({
                    "id": deck_name_id.id,
                    "name": deck_name_id.name
                })

            return {
                "success": True,
                "decks": decks,
                "count": len(decks)
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def create_deck_tool(deck_name: str, collection_path: Optional[str] = None) -> dict:
    """Create a new deck.

    Args:
        deck_name: Name for the new deck.
        collection_path: Path to the collection file. If None, uses the default collection.

    Returns:
        Dict with 'success' (bool), 'message' (str), 'deck_id' (int) or 'error' (str).
    """
    manager = get_manager()
    try:
        with manager.get_collection(collection_path) as col:
            deck_id = col.decks.add_normal_deck_with_name(deck_name).id
            return {
                "success": True,
                "message": f"Deck '{deck_name}' created successfully",
                "deck_id": deck_id
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def list_note_types_tool(collection_path: Optional[str] = None) -> dict:
    """List all note types in the collection.

    Args:
        collection_path: Path to the collection file. If None, uses the default collection.

    Returns:
        Dict with 'success' (bool), 'note_types' (list with id, name, fields), 'count' (int) or 'error' (str).
    """
    manager = get_manager()
    try:
        with manager.get_collection(collection_path) as col:
            note_types = []
            for notetype_name_id in col.models.all_names_and_ids():
                # Get full note type to include field information
                notetype = col.models.get(notetype_name_id.id)
                fields = [field['name'] for field in notetype['flds']]

                note_types.append({
                    "id": notetype_name_id.id,
                    "name": notetype_name_id.name,
                    "fields": fields
                })

            return {
                "success": True,
                "note_types": note_types,
                "count": len(note_types)
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def create_note_tool(
    deck_name: str,
    note_type_name: str,
    fields: dict[str, str],
    tags: list[str] = None,
    collection_path: Optional[str] = None
) -> dict:
    """Create a new note (flashcard).

    Args:
        deck_name: Name of the deck where the note will be added.
        note_type_name: Name of the note type (e.g., 'Basic', 'Cloze').
        fields: Dictionary mapping field names to values (e.g., {'Front': 'Question', 'Back': 'Answer'}).
        tags: Optional list of tags to add to the note.
        collection_path: Path to the collection file. If None, uses the default collection.

    Returns:
        Dict with 'success' (bool), 'message' (str), 'note_id' (int), 'card_count' (int) or 'error' (str).
    """
    manager = get_manager()
    if tags is None:
        tags = []

    try:
        with manager.get_collection(collection_path) as col:
            # Get note type
            notetype = col.models.by_name(note_type_name)
            if not notetype:
                return {
                    "success": False,
                    "error": f"Note type '{note_type_name}' not found",
                    "available_note_types": [nt.name for nt in col.models.all_names_and_ids()]
                }

            # Get deck
            deck_id = col.decks.id_for_name(deck_name)
            if not deck_id:
                return {
                    "success": False,
                    "error": f"Deck '{deck_name}' not found",
                    "available_decks": [d.name for d in col.decks.all_names_and_ids()]
                }

            # Create note
            note = col.new_note(notetype)

            # Set fields
            for field_name, value in fields.items():
                try:
                    note[field_name] = value
                except KeyError:
                    available_fields = [field['name'] for field in notetype['flds']]
                    return {
                        "success": False,
                        "error": f"Field '{field_name}' not found in note type '{note_type_name}'",
                        "available_fields": available_fields
                    }

            # Set tags
            for tag in tags:
                note.add_tag(tag)

            # Add to collection
            col.add_note(note, deck_id)

            return {
                "success": True,
                "message": f"Note created successfully in deck '{deck_name}'",
                "note_id": note.id,
                "card_count": len(note.cards())
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def search_notes_tool(
    query: str,
    limit: int = 100,
    collection_path: Optional[str] = None
) -> dict:
    """Search for notes using Anki search syntax.

    Args:
        query: Anki search query (e.g., 'deck:MyDeck', 'tag:important', 'front:*python*').
        limit: Maximum number of results to return. Default is 100.
        collection_path: Path to the collection file. If None, uses the default collection.

    Returns:
        Dict with 'success' (bool), 'note_ids' (list), 'count' (int), 'query' (str) or 'error' (str).
    """
    manager = get_manager()
    try:
        with manager.get_collection(collection_path) as col:
            note_ids = col.find_notes(query)

            # Apply limit
            if limit and limit > 0:
                note_ids = note_ids[:limit]

            return {
                "success": True,
                "note_ids": note_ids,
                "count": len(note_ids),
                "query": query
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def get_note_tool(note_id: int, collection_path: Optional[str] = None) -> dict:
    """Get detailed information about a specific note.

    Args:
        note_id: ID of the note to retrieve.
        collection_path: Path to the collection file. If None, uses the default collection.

    Returns:
        Dict with 'success' (bool), 'note' (dict with id, fields, tags, etc.) or 'error' (str).
    """
    manager = get_manager()
    try:
        with manager.get_collection(collection_path) as col:
            note = col.get_note(note_id)

            # Get note type
            notetype = note.note_type()

            # Build fields dictionary
            fields = {}
            for i, field_name in enumerate(col.models.field_names(notetype)):
                fields[field_name] = note.fields[i] if i < len(note.fields) else ""

            # Get card info
            cards = note.cards()
            deck_id = cards[0].did if cards else None
            deck_name = col.decks.get(deck_id)['name'] if deck_id else None

            return {
                "success": True,
                "note": {
                    "id": note.id,
                    "guid": note.guid,
                    "note_type_id": note.mid,
                    "note_type_name": notetype['name'],
                    "deck_id": deck_id,
                    "deck_name": deck_name,
                    "fields": fields,
                    "tags": note.tags,
                    "card_ids": [card.id for card in cards]
                }
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def update_note_tool(
    note_id: int,
    fields: Optional[dict[str, str]] = None,
    tags: Optional[list[str]] = None,
    collection_path: Optional[str] = None
) -> dict:
    """Update an existing note's fields and/or tags.

    Args:
        note_id: ID of the note to update.
        fields: Optional dictionary mapping field names to new values.
        tags: Optional list of tags (replaces all existing tags).
        collection_path: Path to the collection file. If None, uses the default collection.

    Returns:
        Dict with 'success' (bool), 'message' (str) or 'error' (str).
    """
    manager = get_manager()
    try:
        with manager.get_collection(collection_path) as col:
            note = col.get_note(note_id)

            # Update fields if provided
            if fields:
                for field_name, value in fields.items():
                    try:
                        note[field_name] = value
                    except KeyError:
                        notetype = note.note_type()
                        available_fields = [field['name'] for field in notetype['flds']]
                        return {
                            "success": False,
                            "error": f"Field '{field_name}' not found",
                            "available_fields": available_fields
                        }

            # Update tags if provided
            if tags is not None:
                # Clear existing tags
                for tag in list(note.tags):
                    note.remove_tag(tag)
                # Add new tags
                for tag in tags:
                    note.add_tag(tag)

            # Save changes
            col.update_note(note)

            return {
                "success": True,
                "message": "Note updated successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
