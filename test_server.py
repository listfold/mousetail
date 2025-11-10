#!/usr/bin/env python3
"""Simple test script to verify the Anki MCP server is working."""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ankimcp.server.collection_manager import get_manager


async def test_collection_manager():
    """Test the collection manager."""
    print("Testing Collection Manager...")
    print("-" * 50)

    manager = get_manager()

    # List available collections
    print("\n1. Listing available collections:")
    collections = manager.list_available_collections()
    if collections:
        for col in collections:
            print(f"   - {col['profile']}: {col['path']}")
    else:
        print("   No collections found on this system")
        print("   This is normal if Anki has never been run")

    print("\n✓ Collection Manager test completed")


async def test_mcp_tools():
    """Test MCP tools."""
    print("\n\nTesting MCP Tools...")
    print("-" * 50)

    from ankimcp.mcp.tools import list_collections_tool, list_decks_tool

    # Test list_collections
    print("\n1. Testing list_collections tool:")
    result = await list_collections_tool()
    print(f"   Result: {result}")

    print("\n✓ MCP Tools test completed")


async def test_mcp_server():
    """Test MCP server creation."""
    print("\n\nTesting MCP Server...")
    print("-" * 50)

    from ankimcp.mcp.server import AnkiMCPServer

    print("\n1. Creating MCP server...")
    server = AnkiMCPServer()
    mcp_server = server.get_server()

    print(f"   Server name: {mcp_server.name}")
    print("\n✓ MCP Server test completed")


async def main():
    """Run all tests."""
    print("=" * 50)
    print("Anki MCP Server - Test Suite")
    print("=" * 50)

    try:
        await test_collection_manager()
        await test_mcp_tools()
        await test_mcp_server()

        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)

        print("\nNext steps:")
        print("1. Start the MCP server:")
        print("   uv run python -m ankimcp.mcp.stdio_server")
        print("\n2. Configure Claude Desktop:")
        print("   Edit ~/Library/Application Support/Claude/claude_desktop_config.json")
        print("   Add:")
        print("   {")
        print('     "mcpServers": {')
        print('       "anki": {')
        print('         "command": "uv",')
        print('         "args": ["run", "python", "-m", "ankimcp.mcp.stdio_server"],')
        print(f'         "cwd": "{Path.cwd()}"')
        print("       }")
        print("     }")
        print("   }")
        print("\n3. Restart Claude Desktop")
        print("\n4. Ask Claude to interact with your Anki:")
        print('   "List my Anki decks"')
        print('   "Create a flashcard in my Spanish deck"')

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
