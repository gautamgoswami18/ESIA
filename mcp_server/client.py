from langchain_mcp_adapters.client import MultiServerMCPClient


class MCPClient:

    def __init__(self):

        self.client = MultiServerMCPClient(
            {
                "esia": {
                    "command": "python",
                    "args": [
                        "-m",
                        "mcp_server.server"
                    ],
                    "transport": "stdio"
                }
            }
        )

    async def get_tools(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>Called MCP Client")
        return await self.client.get_tools()