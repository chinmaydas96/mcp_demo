# MCP Demo Project

This project demonstrates a client-server architecture using MCP (Model Control Protocol) with both SSE (Server-Sent Events) and stdio transport options. It includes tools for web content extraction, BMI calculation, and SQL query execution.

## Project Structure

- `mcp_server.py`: The server implementation with various tools and resources
- `mcp_client.py`: The client implementation that communicates with the server

## Features

### Server Components
1. **Tools**
   - Web Content Extraction: Extracts text content from websites
   - BMI Calculator: Calculates Body Mass Index given weight and height
   - Database Operations: Executes SQL queries safely
   - All tools are registered using `@mcp.tool` decorator

2. **Resources**
   - Database Schema: Exposes database schema as a resource using `@mcp.resource`
   - Resources are accessible via `schema://main` URI

3. **Prompts**
   - SQL Generation: Uses `@mcp.prompt` to generate SQL from natural language
   - Prompts are registered and can be listed/accessed by clients

### Client Features
- Supports both SSE and stdio transport methods
- Communicates with OpenAI's GPT-4 for SQL generation
- Executes database queries and displays results
- Can list and access all server tools, resources, and prompts
- Uses `ClientSession` to interact with server components

## Server-Client Interaction

The server exposes three main types of components that the client can consume:

1. **Tools**
   - Server registers tools using `@mcp.tool` decorator
   - Client can list tools using `session.list_tools()`
   - Tools can be called using `session.call_tool()`

2. **Resources**
   - Server defines resources using `@mcp.resource` decorator
   - Client can read resources using `session.read_resource()`
   - Resources are identified by URIs (e.g., `schema://main`)

3. **Prompts**
   - Server registers prompts using `@mcp.prompt` decorator
   - Client can list prompts using `session.list_prompts()`
   - Prompts can be accessed using `session.get_prompt()`

## Setup

1. Install dependencies:
```bash
pip install openai mcp beautifulsoup4 httpx
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY="your-api-key"
```

3. Ensure you have an SQLite database named `ecommerce.db` in your project directory

## Running the Project

1. Start the server:
```bash
python mcp_server.py
```

2. Run the client:
```bash
python mcp_client.py
```

## Configuration

The server can be configured to run in different modes:
- SSE transport (default): Runs on port 8080 with `/sse` endpoint
- Stdio transport: For direct process communication

## Example Usage

The client can be used to:
- Extract web content from URLs
- Calculate BMI values
- Generate and execute SQL queries
- Access database schema information
- List and use all available server tools, resources, and prompts

## Dependencies

- openai
- mcp
- beautifulsoup4
- httpx
- sqlite3 (built-in)

## License

[Add your license information here]
