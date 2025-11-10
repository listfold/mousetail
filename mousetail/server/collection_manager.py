"""Collection Manager for Anki MCP Server.

Handles opening, closing, and managing Anki collection instances.
Supports multiple collections and thread-safe access.
"""

import os
import threading
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from anki.collection import Collection
from anki.errors import AnkiError


class CollectionManager:
    """Manages Anki collection lifecycle and access."""

    def __init__(self):
        self._collections: dict[str, Collection] = {}
        self._locks: dict[str, threading.RLock] = {}
        self._global_lock = threading.RLock()

    def _get_default_collection_path(self) -> Optional[str]:
        """Get the default Anki collection path for the current platform."""
        home = Path.home()

        # Platform-specific default paths
        if os.name == 'nt':  # Windows
            base_path = home / "AppData" / "Roaming" / "Anki2"
        elif os.name == 'posix':
            if os.uname().sysname == 'Darwin':  # macOS
                base_path = home / "Library" / "Application Support" / "Anki2"
            else:  # Linux
                base_path = home / ".local" / "share" / "Anki2"
        else:
            return None

        # Look for User 1 profile (default)
        default_profile = base_path / "User 1" / "collection.anki2"
        if default_profile.exists():
            return str(default_profile)

        # Try to find any collection
        if base_path.exists():
            for profile_dir in base_path.iterdir():
                if profile_dir.is_dir():
                    collection_file = profile_dir / "collection.anki2"
                    if collection_file.exists():
                        return str(collection_file)

        return None

    def list_available_collections(self) -> list[dict[str, str]]:
        """List all available Anki collections on the system.

        Returns:
            List of dicts with 'profile' and 'path' keys
        """
        collections = []
        home = Path.home()

        # Platform-specific base paths
        if os.name == 'nt':  # Windows
            base_path = home / "AppData" / "Roaming" / "Anki2"
        elif os.name == 'posix':
            if os.uname().sysname == 'Darwin':  # macOS
                base_path = home / "Library" / "Application Support" / "Anki2"
            else:  # Linux
                base_path = home / ".local" / "share" / "Anki2"
        else:
            return collections

        if base_path.exists():
            for profile_dir in base_path.iterdir():
                if profile_dir.is_dir():
                    collection_file = profile_dir / "collection.anki2"
                    if collection_file.exists():
                        collections.append({
                            'profile': profile_dir.name,
                            'path': str(collection_file)
                        })

        return collections

    def open_collection(self, path: Optional[str] = None) -> str:
        """Open a collection and return its path identifier.

        Args:
            path: Path to collection file. If None, uses default.

        Returns:
            Collection path (identifier)

        Raises:
            ValueError: If path is invalid or collection doesn't exist
            AnkiError: If collection cannot be opened
        """
        if path is None:
            path = self._get_default_collection_path()
            if path is None:
                raise ValueError("No default collection found. Please specify a path.")

        path = str(Path(path).resolve())

        if not os.path.exists(path):
            raise ValueError(f"Collection file does not exist: {path}")

        with self._global_lock:
            if path not in self._collections:
                try:
                    col = Collection(path)
                    self._collections[path] = col
                    self._locks[path] = threading.RLock()
                except Exception as e:
                    raise AnkiError(f"Failed to open collection: {e}")

        return path

    def close_collection(self, path: str):
        """Close a collection.

        Args:
            path: Path to collection file
        """
        with self._global_lock:
            if path in self._collections:
                col = self._collections[path]
                with self._locks[path]:
                    col.close()
                del self._collections[path]
                del self._locks[path]

    def close_all(self):
        """Close all open collections."""
        with self._global_lock:
            paths = list(self._collections.keys())
            for path in paths:
                self.close_collection(path)

    @contextmanager
    def get_collection(self, path: Optional[str] = None):
        """Get a collection with thread-safe access.

        Args:
            path: Path to collection. If None, uses default or first open collection.

        Yields:
            Collection instance

        Example:
            >>> manager = CollectionManager()
            >>> with manager.get_collection() as col:
            ...     note = col.new_note(notetype)
        """
        if path is None:
            # Try to find an open collection
            with self._global_lock:
                if self._collections:
                    path = next(iter(self._collections.keys()))
                else:
                    # Open default collection
                    path = self.open_collection()

        path = str(Path(path).resolve()) if path else path

        # Ensure collection is open
        if path not in self._collections:
            path = self.open_collection(path)

        with self._locks[path]:
            yield self._collections[path]

    def get_collection_info(self, path: Optional[str] = None) -> dict:
        """Get information about a collection.

        Args:
            path: Path to collection. If None, uses default.

        Returns:
            Dict with collection information
        """
        with self.get_collection(path) as col:
            return {
                'path': path,
                'name': col.name(),
                'card_count': col.card_count(),
                'note_count': col.note_count(),
                'is_empty': col.is_empty(),
            }


# Global collection manager instance
_manager: Optional[CollectionManager] = None
_manager_lock = threading.Lock()


def get_manager() -> CollectionManager:
    """Get the global collection manager instance."""
    global _manager
    if _manager is None:
        with _manager_lock:
            if _manager is None:
                _manager = CollectionManager()
    return _manager
