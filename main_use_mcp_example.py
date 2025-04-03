#smithery 에서 제공하는 도구를 JSON 형식으로 가져올때, 아래의 예시처럼 "transport": "stdio" 로 설정

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

model = ChatAnthropic(model="claude-3-7-sonnet-latest", temperature=0, max_tokens=20000)

client = MultiServerMCPClient(
    {
        "server-sequential-thinking": {
            "command": "npx",
            "args": [
                "-y",
                "@smithery/cli@latest",
                "run",
                "@smithery-ai/server-sequential-thinking",
                "--key",
                "89a4780a-53b7-4b7b-92e9-a29815f2669b",
            ],
            "transport": "stdio",
        },
        "desktop-commander": {
            "command": "npx",
            "args": [
                "-y",
                "@smithery/cli@latest",
                "run",
                "@wonderwhy-er/desktop-commander",
                "--key",
                "89a4780a-53b7-4b7b-92e9-a29815f2669b",
            ],
            "transport": "stdio",
        },
        "document-retriever": {
            "command": "./.venv/bin/python",
            "args": ["./mcp_server_rag.py"],
            "transport": "stdio",
        },
    }
)


# ipynb 의 사용 코드
await client.__aenter__()

agent = create_react_agent(model, client.get_tools(), checkpointer=MemorySaver())

await astream_graph(
    agent,
    {
        "messages": "현재 경로를 포함한 하위 폴더 구조를 tree 로 그려줘. 단, .venv 폴더는 제외하고 출력해줘."
    },
    config=config,
)

await astream_graph(
    agent,
    {
        "messages": (
            "`retriever` 도구를 사용해서 삼성전자가 개발한 생성형 AI 관련 내용을 검색하고 "
            "`Sequential Thinking` 도구를 사용해서 보고서를 작성해줘."
        )
    },
    config=config,
)

await astream_graph(
    agent, {"messages": "이전의 내용을 bullet point 로 요약해줘"}, config=config
)