# MCP Capabilities Checker

A simple Python client for inspecting Model Context Protocol (MCP) server capabilities.

This tool connects to an MCP server and retrieves information about its capabilities, including:
- Server name and version
- Available capabilities (prompts, resources, tools)
- List of available prompts with their arguments
- List of available resources
- List of available tools with their arguments

The output is presented in YAML format, either to stdout or a specified file.

> **Note:** Currently, the tool only connects to MCP servers via stdio. Support for SSE/HTTP connections is planned for future development.

> **Note:** This application is itself an MCP client and can be used to "ping" MCP servers to verify they are operational and inspect their capabilities.

## Installation

### Using uv (recommended)

```bash
uv pip install .
```

### Using pip

```bash
pip install .
```

## Usage

Basic usage:

```bash
mcp-capabilities-checker <command> [args...]
```

Where:
- `<command>` is the MCP server command to execute
- `[args...]` are optional arguments for the server command

Example:

```bash
# Run a local server
mcp-capabilities-checker python my_mcp_server.py

# Save output to a file
mcp-capabilities-checker python my_mcp_server.py --output capabilities.yaml
```

## Example Output

```yaml
serverName: ExampleServer
serverVersion: 1.6.0
serverCapabilities:
  prompts: true
  resources: true
  tools: true
prompts:
  prompts:
  - name: example_prompt
    description: An example prompt template
    arguments:
    - name: arg1
      description: null
      required: true
resources:
  resources:
  - uri: file://example/
    name: file://example/
    description: null
    mimeType: text/plain
    size: null
    annotations: null
tools:
  tools:
  - name: example_tool
    description: An example tool
    inputSchema:
      properties:
        arg1:
          title: Arg1
          type: string
      required:
      - arg1
      title: example_toolArguments
      type: object
```

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   uv pip install -e .
   ```
3. Run the tool:
   ```bash
   uv run python mcp_capabilities_checker/main.py <command> [args...]
   ```

Example:
```bash
uv run mcp-capabilities-checker uv run python examples/example_server.py
```

## License

MIT 