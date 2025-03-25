import asyncio
from pathlib import Path

from src.management_file.domain.service.file_server import FileServer

def main():
    base_path = Path("./_reference/workspace")  # 작업 디렉토리 지정
    server = FileServer(base_path)
    server.setup_handlers()
    server.server.run()  # 동기 메서드로 실행

if __name__ == "__main__":
    main()