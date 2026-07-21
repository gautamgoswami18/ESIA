from app.mcp.registry import MCPRegistry


registry = MCPRegistry()


def hello(name):

    return f"Hello {name}"


registry.register(
    "hello",
    hello
)

print(
    registry.execute(
        "hello",
        name="Gautam"
    )
)

print(
    registry.list_tools()
)