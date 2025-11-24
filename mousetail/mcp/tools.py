"""Tool implementations for MCP server.

This module contains the actual implementation of each MCP tool exposed
by the Anki MCP server. Each function corresponds to a tool that LLMs
can call to interact with Anki collections.
"""

import json
import keyring
from pathlib import Path
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

    # Check if any collection is accessible (fail fast if Anki is running)
    collections = manager.list_available_collections()
    if collections:
        try:
            # Try the first collection to check accessibility
            manager.check_collection_accessible(collections[0]['path'])
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

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
        # Check accessibility first
        manager.check_collection_accessible(collection_path)
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
        # Check accessibility first
        manager.check_collection_accessible(collection_path)
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
        # Check accessibility first
        manager.check_collection_accessible(collection_path)
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
        # Check accessibility first
        manager.check_collection_accessible(collection_path)
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
        # Check accessibility first
        manager.check_collection_accessible(collection_path)
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
        # Check accessibility first
        manager.check_collection_accessible(collection_path)
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
        # Check accessibility first
        manager.check_collection_accessible(collection_path)
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
        # Check accessibility first
        manager.check_collection_accessible(collection_path)
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


# Sync-related helper functions and tools

KEYRING_SERVICE_NAME = "mousetail-anki-sync"


def _load_config() -> dict:
    """Load configuration from config.json.

    Returns:
        Dict with configuration data, or empty dict if file doesn't exist.
    """
    try:
        # Look for config.json in the project root
        config_path = Path(__file__).parent.parent.parent / "config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _get_sync_endpoint_from_config() -> Optional[str]:
    """Get the preferred sync endpoint from config.

    Returns:
        Endpoint URL string or None for AnkiWeb.
    """
    config = _load_config()
    return config.get("sync", {}).get("endpoint")


async def save_sync_credentials_tool(
    username: str,
    password: str,
    endpoint: Optional[str] = None
) -> dict:
    """Save sync credentials securely to system keychain.

    Stores credentials using the system's secure credential storage:
    - macOS: Keychain
    - Windows: Credential Manager
    - Linux: Secret Service (GNOME Keyring, KWallet, etc.)

    Args:
        username: AnkiWeb ID or sync server username.
        password: Account password.
        endpoint: Optional sync server URL (saved separately). Leave empty for AnkiWeb.

    Returns:
        Dict with 'success' (bool), 'message' (str) or 'error' (str).
    """
    try:
        # Save username and password to keychain
        keyring.set_password(KEYRING_SERVICE_NAME, "username", username)
        keyring.set_password(KEYRING_SERVICE_NAME, username, password)

        # Save endpoint if provided
        if endpoint:
            keyring.set_password(KEYRING_SERVICE_NAME, "endpoint", endpoint)
        else:
            # Clear endpoint if None (use AnkiWeb)
            try:
                keyring.delete_password(KEYRING_SERVICE_NAME, "endpoint")
            except keyring.errors.PasswordDeleteError:
                pass

        endpoint_msg = f" with endpoint '{endpoint}'" if endpoint else " for AnkiWeb"
        return {
            "success": True,
            "message": f"Credentials saved securely for user '{username}'{endpoint_msg}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to save credentials: {str(e)}"
        }


async def load_sync_credentials_tool() -> dict:
    """Load saved sync credentials from system keychain.

    Returns:
        Dict with 'success' (bool), 'username' (str), 'password' (str),
        'endpoint' (str or None), or 'error' (str).
    """
    try:
        # Load username
        username = keyring.get_password(KEYRING_SERVICE_NAME, "username")
        if not username:
            return {
                "success": False,
                "error": "No saved credentials found. Use save_sync_credentials first."
            }

        # Load password
        password = keyring.get_password(KEYRING_SERVICE_NAME, username)
        if not password:
            return {
                "success": False,
                "error": f"Password not found for user '{username}'"
            }

        # Load endpoint (may be None for AnkiWeb)
        endpoint = keyring.get_password(KEYRING_SERVICE_NAME, "endpoint")

        return {
            "success": True,
            "username": username,
            "password": password,
            "endpoint": endpoint
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to load credentials: {str(e)}"
        }


async def delete_sync_credentials_tool() -> dict:
    """Delete saved sync credentials from system keychain.

    Returns:
        Dict with 'success' (bool), 'message' (str) or 'error' (str).
    """
    try:
        # Get username first
        username = keyring.get_password(KEYRING_SERVICE_NAME, "username")

        if username:
            # Delete password
            try:
                keyring.delete_password(KEYRING_SERVICE_NAME, username)
            except keyring.errors.PasswordDeleteError:
                pass

            # Delete username
            try:
                keyring.delete_password(KEYRING_SERVICE_NAME, "username")
            except keyring.errors.PasswordDeleteError:
                pass

        # Delete endpoint
        try:
            keyring.delete_password(KEYRING_SERVICE_NAME, "endpoint")
        except keyring.errors.PasswordDeleteError:
            pass

        return {
            "success": True,
            "message": "Credentials deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete credentials: {str(e)}"
        }


async def sync_collection_tool(
    username: Optional[str] = None,
    password: Optional[str] = None,
    endpoint: Optional[str] = None,
    sync_media: bool = True,
    collection_path: Optional[str] = None
) -> dict:
    """Synchronize Anki collection with AnkiWeb or a self-hosted sync server.

    This tool uploads local changes and downloads remote changes to keep your
    collection in sync. By default, it syncs both the collection data (cards,
    notes, decks) and media files (images, audio).

    Authentication priority:
    1. Credentials passed as parameters
    2. Saved credentials from keychain
    3. Error if no credentials available

    Endpoint priority:
    1. Endpoint parameter (if provided)
    2. Saved endpoint from keychain
    3. Endpoint from config.json
    4. AnkiWeb (default)

    Args:
        username: AnkiWeb ID or sync server username (optional if saved).
        password: Account password (optional if saved).
        endpoint: Sync server URL (optional). Examples:
                  - None or empty: Use AnkiWeb (default)
                  - "https://sync.example.com": Use self-hosted server
        sync_media: Include media files in sync (default: True).
        collection_path: Path to collection file (optional, uses default if not provided).

    Returns:
        Dict with 'success' (bool), 'message' (str), 'required' (str) or 'error' (str).
    """
    manager = get_manager()

    try:
        # Determine credentials to use
        if not username or not password:
            # Try to load from keychain
            creds_result = await load_sync_credentials_tool()
            if not creds_result.get("success"):
                return {
                    "success": False,
                    "error": "No credentials provided and no saved credentials found",
                    "required": "Please provide username and password, or use save_sync_credentials first"
                }

            username = username or creds_result.get("username")
            password = password or creds_result.get("password")

            # Use saved endpoint if not provided
            if endpoint is None and creds_result.get("endpoint"):
                endpoint = creds_result.get("endpoint")

        # Determine endpoint to use
        if endpoint is None:
            # Try config.json
            endpoint = _get_sync_endpoint_from_config()

        # Convert empty string to None (for AnkiWeb)
        if endpoint == "":
            endpoint = None

        # Check collection accessibility
        manager.check_collection_accessible(collection_path)

        with manager.get_collection(collection_path) as col:
            # Authenticate
            try:
                auth = col.sync_login(username, password, endpoint)
            except Exception as e:
                error_msg = str(e)
                if "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
                    return {
                        "success": False,
                        "error": f"Authentication failed: {error_msg}",
                        "hint": "Please check your username and password"
                    }
                elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                    return {
                        "success": False,
                        "error": f"Network error: {error_msg}",
                        "hint": "Please check your internet connection and endpoint URL"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Login failed: {error_msg}"
                    }

            # Perform sync
            try:
                output = col.sync_collection(auth, sync_media=sync_media)

                # Parse sync output
                endpoint_str = f" with {endpoint}" if endpoint else " with AnkiWeb"
                media_str = " (including media)" if sync_media else " (collection only)"

                return {
                    "success": True,
                    "message": f"Collection synced successfully{endpoint_str}{media_str}",
                    "output": str(output)
                }
            except Exception as e:
                error_msg = str(e)
                return {
                    "success": False,
                    "error": f"Sync failed: {error_msg}",
                    "hint": "Check for conflicts or try syncing from Anki desktop first"
                }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
