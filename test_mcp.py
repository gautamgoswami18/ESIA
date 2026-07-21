import asyncio

from mcp_server.client import MCPClient


async def main():

    client = MCPClient()

    tools = await client.get_tools()

    print("=" * 80)

    for tool in tools:
        print(tool.name)

    print("=" * 80)


asyncio.run(main())