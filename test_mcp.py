import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp():
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Test greeting resource
            print("\nTesting greeting resource:")
            greeting = await session.read_resource("greeting://John")
            print(f"Greeting result: {greeting}")

            # Test calculate tool
            print("\nTesting calculate tool:")
            result = await session.call_tool(
                "calculate",
                arguments={
                    "operation": "add",
                    "a": 5,
                    "b": 3
                }
            )
            print(f"Calculation result: {result}")

            # Test response prompt
            print("\nTesting response prompt:")
            prompt = await session.get_prompt(
                "generate_response",
                arguments={"input_text": "Hello, how are you?"}
            )
            print(f"Prompt result: {prompt}")

if __name__ == "__main__":
    asyncio.run(test_mcp()) 