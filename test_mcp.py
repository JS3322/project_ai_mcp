import pytest
import pytest_asyncio
import os
import shutil
from datetime import datetime, time
from schedule_repository import Schedule, SchedulePriority, CSVScheduleRepository
from main import get_today_schedule, add_schedule

TEST_DATA_DIR = "_reference/test_data"
TEST_CSV_PATH = f"{TEST_DATA_DIR}/test_schedules.csv"

@pytest_asyncio.fixture(autouse=True)
async def setup_test_data():
    """테스트용 CSV 파일을 설정하고 초기 데이터를 생성합니다."""
    # 테스트 디렉토리 생성
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    
    # 기존 테스트 파일이 있다면 삭제
    if os.path.exists(TEST_CSV_PATH):
        os.remove(TEST_CSV_PATH)
    
    # 실제 데이터 파일을 테스트 파일로 복사
    shutil.copy("_reference/data/schedules.csv", TEST_CSV_PATH)
    
    yield
    
    # 테스트 후 정리
    try:
        if os.path.exists(TEST_CSV_PATH):
            os.remove(TEST_CSV_PATH)
        if os.path.exists(TEST_DATA_DIR):
            os.rmdir(TEST_DATA_DIR)
    except Exception as e:
        print(f"테스트 파일 정리 중 오류 발생: {e}")

@pytest.mark.asyncio
async def test_get_today_schedule():
    """오늘의 스케줄 조회 테스트"""
    # 스케줄 조회
    schedule_summary = await get_today_schedule()
    
    # 기본 포맷 검증
    assert "📅 오늘의 스케줄 요약" in schedule_summary
    assert "🔴" in schedule_summary  # 높은 우선순위 일정 확인
    assert "아침 회의" in schedule_summary  # 기본 데이터 확인

@pytest.mark.asyncio
async def test_add_schedule():
    """스케줄 추가 테스트"""
    # 새 스케줄 추가
    result = await add_schedule(
        title="테스트 미팅",
        description="테스트 목적의 미팅",
        start_hour=13,
        start_minute=0,
        end_hour=14,
        end_minute=30,
        priority="high"
    )
    
    # 성공 메시지 확인
    assert "✅" in result
    assert "테스트 미팅" in result
    
    # 잘못된 우선순위로 추가 시도
    invalid_result = await add_schedule(
        title="실패할 미팅",
        description="잘못된 우선순위",
        start_hour=15,
        start_minute=0,
        end_hour=16,
        end_minute=0,
        priority="invalid"
    )
    
    # 실패 메시지 확인
    assert "❌" in invalid_result

@pytest.mark.asyncio
async def test_schedule_integration():
    """스케줄 추가 후 조회 통합 테스트"""
    # 새 스케줄 추가
    await add_schedule(
        title="통합 테스트 미팅",
        description="통합 테스트용 미팅",
        start_hour=10,
        start_minute=0,
        end_hour=11,
        end_minute=0,
        priority="medium"
    )
    
    # 스케줄 목록 조회
    schedule_summary = await get_today_schedule()
    
    # 추가된 스케줄 확인
    assert "통합 테스트 미팅" in schedule_summary
    assert "🟡" in schedule_summary  # 중간 우선순위 확인

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 