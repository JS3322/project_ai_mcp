import pytest
from pathlib import Path
import asyncio
import tempfile
import shutil
from main_file import main
from src.management_file.domain.service.file_server import FileServer

@pytest.fixture
def temp_workspace():
    """임시 작업 디렉토리를 생성하는 fixture"""
    temp_dir = tempfile.mkdtemp()
    workspace = Path(temp_dir) / "workspace"
    workspace.mkdir(parents=True)
    yield workspace
    shutil.rmtree(temp_dir)

@pytest.fixture
def file_server(temp_workspace):
    """FileServer 인스턴스를 생성하는 fixture"""
    server = FileServer(temp_workspace)
    server.setup_handlers()
    return server

def test_main_creates_file_server(monkeypatch, temp_workspace):
    """main 함수가 FileServer를 올바르게 생성하는지 테스트"""
    # FileServer.run이 호출되었는지 확인하기 위한 mock
    class MockServer:
        def __init__(self):
            self.run_called = False
        
        def run(self):
            self.run_called = True
    
    mock_server = MockServer()
    
    class MockFileServer:
        def __init__(self, base_path):
            self.base_path = base_path
            self.server = mock_server
            self.handlers_setup = False
        
        def setup_handlers(self):
            self.handlers_setup = True
    
    # FileServer 클래스를 mock으로 대체
    monkeypatch.setattr("main_file.FileServer", MockFileServer)
    
    # 작업 디렉토리 경로를 임시 디렉토리로 변경
    monkeypatch.setattr("main_file.Path", lambda x: temp_workspace)
    
    # main 함수 실행
    main()
    
    # 검증
    assert mock_server.run_called, "서버의 run 메서드가 호출되지 않았습니다"

def test_file_server_setup(file_server, temp_workspace):
    """FileServer가 올바르게 설정되었는지 테스트"""
    assert file_server.fs.base_path == temp_workspace
    assert hasattr(file_server, 'server'), "서버 인스턴스가 없습니다"
    assert hasattr(file_server.server, 'resources'), "리소스 핸들러가 설정되지 않았습니다"
    assert hasattr(file_server.server, 'tools'), "도구 핸들러가 설정되지 않았습니다"

def test_workspace_directory_structure(temp_workspace):
    """작업 디렉토리 구조가 올바른지 테스트"""
    assert temp_workspace.exists()
    assert temp_workspace.is_dir() 