import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_schedule_server():
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["main.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # 1. 오늘의 스케줄 확인
            print("\n=== 오늘의 스케줄 ===")
            schedules = await session.read_resource("schedule://today")
            print(f"스케줄 결과: {schedules}")

            # 2. 새로운 스케줄 추가
            print("\n=== 스케줄 추가 ===")
            schedule_data = {
                "title": "팀 미팅",
                "description": "주간 스프린트 미팅",
                "start_hour": 10,
                "start_minute": 0,
                "end_hour": 11,
                "end_minute": 0,
                "priority": "high"
            }
            result = await session.call_tool(
                "add_schedule",
                arguments=schedule_data
            )
            print(f"스케줄 추가 결과: {result}")

if __name__ == "__main__":
    asyncio.run(test_schedule_server()) 