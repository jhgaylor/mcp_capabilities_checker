import argparse
import asyncio
import yaml
import sys

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

def clean(data, fields_to_remove=["meta", "nextCursor"]):
    """
    Remove specified fields from the top level of a dictionary.
    
    Args:
        data (dict): The dictionary to clean
        fields_to_remove (list, optional): List of field names to remove from the top level.
            Defaults to None.
            
    Returns:
        dict: A new dictionary with the specified fields removed
    """
    if not isinstance(data, dict):
        return data
    
    if fields_to_remove is None:
        return data
    
    return {k: v for k, v in data.items() if k not in fields_to_remove}


async def check_capabilities(server_command, server_args=None):
    """Connect to an MCP server and check its capabilities."""
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command=server_command,
        args=server_args or [],
        env=None,
    )

    output = {}
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            initialize_result = await session.initialize()
            
            # Get server info from the server_info property
            output['serverName'] = initialize_result.serverInfo.name
            output['serverVersion'] = initialize_result.serverInfo.version

            capabilities = initialize_result.capabilities
            
            # Convert capabilities to dict for YAML serialization
            capabilities_dict = {}
            if hasattr(capabilities, "prompts"):
                capabilities_dict["prompts"] = capabilities.prompts is not None
            if hasattr(capabilities, "resources"):
                capabilities_dict["resources"] = capabilities.resources is not None
            if hasattr(capabilities, "tools"):
                capabilities_dict["tools"] = capabilities.tools is not None
            
            output['serverCapabilities'] = capabilities_dict
            
            # Check and list prompts if available
            if capabilities.prompts:
                prompts = await session.list_prompts()
                output['prompts'] = clean(prompts.model_dump(mode='json'))
            
            # Check and list resources if available
            if capabilities.resources:
                resources = await session.list_resources()
                output['resources'] = clean(resources.model_dump(mode='json'))
            
            # Check and list tools if available
            if capabilities.tools:
                tools = await session.list_tools()
                output['tools'] = clean(tools.model_dump(mode='json'))
        
    return output

def main():
    parser = argparse.ArgumentParser(description="Check MCP server capabilities")
    parser.add_argument("command", help="MCP server command to execute")
    parser.add_argument("args", nargs="*", help="Arguments for the MCP server command")
    parser.add_argument("--output", "-o", help="Output file (defaults to stdout)")
    args = parser.parse_args()
    print(args.command)
    print(args.args)

    result = asyncio.run(check_capabilities(args.command, args.args))
    yaml_output = yaml.dump(result, sort_keys=False)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(yaml_output)
    else:
        print("Server Information:")
        print("-" * 40)
        print(yaml_output)


if __name__ == "__main__":
    main() 