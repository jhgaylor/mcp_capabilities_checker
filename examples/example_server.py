from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ExampleServer", version="1.0.0")


@mcp.resource("file://example")
def example_resource() -> str:
    """An example resource"""
    return "This is an example resource content"


@mcp.tool()
def example_tool(arg1: str) -> str:
    """An example tool"""
    return f"Tool executed with arg1: {arg1}"


@mcp.prompt()
def example_prompt(arg1: str) -> str:
    """An example prompt template"""
    return f"This is a prompt with arg1: {arg1}"


if __name__ == "__main__":
    mcp.run() 