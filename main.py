from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Any, List
import asyncio
from schedule_repository import CSVScheduleRepository, Schedule, SchedulePriority
from datetime import datetime, time

# Initialize MCP server and repositories
mcp = FastMCP("Schedule Management Server")
schedule_repository = CSVScheduleRepository()

# 스케줄 관련 리소스 추가
@mcp.resource("schedule://today")
async def get_today_schedule() -> str:
    """오늘의 스케줄을 요약하여 반환합니다."""
    schedules = await schedule_repository.get_todays_schedules()
    
    if not schedules:
        return "오늘 예정된 스케줄이 없습니다."
    
    summary = "📅 오늘의 스케줄 요약:\n\n"
    for schedule in schedules:
        priority_mark = {
            SchedulePriority.HIGH: "🔴",
            SchedulePriority.MEDIUM: "🟡",
            SchedulePriority.LOW: "🟢"
        }.get(schedule.priority, "⚪")
        
        summary += f"{priority_mark} {schedule.start_time.strftime('%H:%M')} - {schedule.end_time.strftime('%H:%M')}\n"
        summary += f"   {schedule.title}\n"
        summary += f"   {schedule.description}\n\n"
    
    return summary

# 스케줄 추가 도구
@mcp.tool()
async def add_schedule(
    title: str,
    description: str,
    start_hour: int,
    start_minute: int,
    end_hour: int,
    end_minute: int,
    priority: str = "medium"
) -> str:
    """새로운 스케줄을 추가합니다."""
    try:
        priority_enum = SchedulePriority(priority.lower())
        new_schedule = Schedule(
            id=0,  # 저장소에서 자동 할당
            title=title,
            description=description,
            start_time=time(start_hour, start_minute),
            end_time=time(end_hour, end_minute),
            priority=priority_enum,
            created_at=datetime.now()
        )
        
        await schedule_repository.add_schedule(new_schedule)
        return f"✅ 새로운 스케줄이 추가되었습니다: {title}"
        
    except ValueError as e:
        return f"❌ 스케줄 추가 실패: {str(e)}"

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()