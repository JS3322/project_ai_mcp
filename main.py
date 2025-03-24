from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

# Initialize MCP server
mcp = FastMCP("Example Server")

# Define a resource for greetings
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"

# Define a tool for calculations
@mcp.tool()
def calculate(operation: str, a: float, b: float) -> Dict[str, Any]:
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None
    }
    
    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")
    
    result = operations[operation](a, b)
    if result is None:
        raise ValueError("Division by zero")
        
    return {
        "result": result,
        "operation": operation,
        "a": a,
        "b": b
    }

# Define a prompt template
@mcp.prompt()
def generate_response(input_text: str) -> str:
    return f"""
    Based on the following input: "{input_text}"
    
    Please provide a helpful and relevant response.
    """

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()