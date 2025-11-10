"""Anki MCP Server - Addon Entry Point.

This addon provides MCP (Model Context Protocol) server capabilities for Anki,
allowing LLMs to interact with Anki collections through a standardized protocol.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Only import Anki GUI modules when running as an addon
try:
    from aqt import mw
    from aqt.qt import QAction
    from aqt.utils import showInfo, tooltip
    IS_ADDON = True
except ImportError:
    IS_ADDON = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ankimcp")


class AnkiMCPAddon:
    """Main addon class for Anki MCP Server."""

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from config.json."""
        addon_dir = Path(__file__).parent
        config_path = addon_dir / "config.json"

        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            logger.warning("config.json not found, using defaults")
            return {
                "collection": {"auto_open_default": True, "default_path": None},
                "logging": {"level": "INFO", "file": None}
            }

    def show_info(self):
        """Show information about the addon."""
        info_text = "Anki MCP Server\n\n"
        info_text += "This addon enables Claude and other LLMs to interact with your Anki collection.\n\n"
        info_text += "To use:\n"
        info_text += "1. Configure Claude Desktop to use the MCP server\n"
        info_text += "2. Add this to claude_desktop_config.json:\n\n"
        info_text += "{\n"
        info_text += '  "mcpServers": {\n'
        info_text += '    "anki": {\n'
        info_text += '      "command": "uv",\n'
        info_text += '      "args": ["run", "python", "-m", "ankimcp.mcp.stdio_server"],\n'
        info_text += '      "cwd": "/path/to/ankimcp"\n'
        info_text += "    }\n"
        info_text += "  }\n"
        info_text += "}\n\n"
        info_text += "MCP Tools available:\n"
        info_text += "- list_collections\n"
        info_text += "- list_decks\n"
        info_text += "- create_deck\n"
        info_text += "- list_note_types\n"
        info_text += "- create_note\n"
        info_text += "- search_notes\n"
        info_text += "- get_note\n"
        info_text += "- update_note\n"

        if IS_ADDON:
            showInfo(info_text)
        else:
            print(info_text)


# Global addon instance
addon_instance = None


def setup_addon():
    """Setup the addon when Anki starts."""
    global addon_instance

    if not IS_ADDON:
        logger.info("Not running as Anki addon")
        return

    addon_instance = AnkiMCPAddon()

    # Add menu item
    action_info = QAction("Anki MCP Info", mw)
    action_info.triggered.connect(addon_instance.show_info)
    mw.form.menuTools.addAction(action_info)

    logger.info("Anki MCP addon initialized")


# Initialize addon when Anki loads
if IS_ADDON:
    from aqt import gui_hooks
    gui_hooks.main_window_did_init.append(lambda: setup_addon())
