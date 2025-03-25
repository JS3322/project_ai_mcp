from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Optional
from enum import Enum
import csv
import os
from pathlib import Path

class SchedulePriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Schedule:
    id: int
    title: str
    description: str
    start_time: time
    end_time: time
    priority: SchedulePriority
    created_at: datetime

class ScheduleRepository(ABC):
    @abstractmethod
    async def get_todays_schedules(self) -> List[Schedule]:
        """오늘의 스케줄 목록을 반환합니다."""
        pass

    @abstractmethod
    async def add_schedule(self, schedule: Schedule) -> Schedule:
        """새로운 스케줄을 추가합니다."""
        pass

class CSVScheduleRepository(ScheduleRepository):
    def __init__(self, csv_path: str = "_reference/data/schedules.csv"):
        self.csv_path = csv_path
        # CSV 파일이 없으면 생성
        if not os.path.exists(csv_path):
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            self._create_empty_csv()

    def _create_empty_csv(self):
        """빈 CSV 파일을 생성합니다."""
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'description', 'start_time', 
                           'end_time', 'priority', 'created_at'])

    def _parse_time(self, time_str: str) -> time:
        """시간 문자열을 파싱합니다."""
        return datetime.strptime(time_str.strip(), "%H:%M").time()

    def _format_time(self, t: time) -> str:
        """time 객체를 문자열로 변환합니다."""
        return t.strftime("%H:%M")

    async def get_todays_schedules(self) -> List[Schedule]:
        """CSV 파일에서 스케줄을 읽어옵니다."""
        schedules = []
        with open(self.csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    schedule = Schedule(
                        id=int(row['id']),
                        title=row['title'].strip(),
                        description=row['description'].strip(),
                        start_time=self._parse_time(row['start_time']),
                        end_time=self._parse_time(row['end_time']),
                        priority=SchedulePriority(row['priority'].strip().lower()),
                        created_at=datetime.strptime(row['created_at'].strip(), 
                                                   "%Y-%m-%d %H:%M:%S")
                    )
                    schedules.append(schedule)
                except (ValueError, KeyError) as e:
                    print(f"스케줄 데이터 파싱 오류: {e}")
                    continue
        return sorted(schedules, key=lambda x: x.start_time)

    async def add_schedule(self, schedule: Schedule) -> Schedule:
        """CSV 파일에 새로운 스케줄을 추가합니다."""
        try:
            # 현재 스케줄 읽기
            schedules = await self.get_todays_schedules()
            
            # 새로운 ID 할당
            if schedules:
                new_id = max(s.id for s in schedules) + 1
            else:
                new_id = 1
            schedule.id = new_id

            # CSV 파일에 추가
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    schedule.id,
                    schedule.title.strip(),
                    schedule.description.strip(),
                    self._format_time(schedule.start_time),
                    self._format_time(schedule.end_time),
                    schedule.priority.value.strip(),
                    schedule.created_at.strftime("%Y-%m-%d %H:%M:%S")
                ])

            return schedule
        except Exception as e:
            raise ValueError(f"스케줄 추가 실패: {str(e)}") 