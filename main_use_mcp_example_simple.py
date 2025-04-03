from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
import asyncio

model = ChatAnthropic(
    model_name="claude-3-7-sonnet-latest", temperature=0, max_tokens=20000
)

client = MultiServerMCPClient(
    {
        "document-retriever": {
            "command": "./.venv/bin/python",
            "args": ["./mcp_server_rag.py"],
            "transport": "stdio",
        },
    }
)

async def main():
    await client.__aenter__()

    prompt = (
        "You are a smart agent. "
        "Answer in Korean."
    )
    agent = create_react_agent(
        model, client.get_tools(), prompt=prompt, checkpointer=MemorySaver()
    )

    config = RunnableConfig(recursion_limit=30, thread_id=1)

    await astream_graph(
        agent,
        {
            "messages": "서울의 날씨는?"
        },
        config=config,
    )

if __name__ == "__main__":
    asyncio.run(main())