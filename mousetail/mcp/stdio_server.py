"""MCP server with stdio transport for Claude Desktop integration."""

import asyncio
import logging
from mcp.server.stdio import stdio_server

from mousetail.mcp.server import AnkiMCPServer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def async_main():
    """Run the MCP server with stdio transport."""
    logger.info("Starting Anki MCP Server with stdio transport")

    anki_server = AnkiMCPServer()
    server = anki_server.get_server()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main():
    """Entry point for the mousetail script."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
