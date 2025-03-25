from pathlib import Path
import mimetypes
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, Tool
from src.management_file.domain.service.file_system_manager import FileSystemManager


class FileServer:
    def __init__(self, base_path: str | Path):
        self.fs = FileSystemManager(base_path)
        self.server = FastMCP("file-server")

    def setup_handlers(self):
        """MCP 핸들러 설정"""
        @self.server.resource("file://{path}")
        async def get_resource(path: str) -> str:
            content, _ = await self.fs.read_file(path)
            return content

        @self.server.tool()
        async def write_file(path: str, content: str) -> str:
            await self.fs.write_file(path, content)
            return f"File written: {path}"

        @self.server.tool()
        async def search_files(pattern: str) -> str:
            results = await self.fs.search_files(pattern)
            return "\n".join(
                f"[{r['type']}] {r['path']}"
                for r in results
            ) or "No files found"
