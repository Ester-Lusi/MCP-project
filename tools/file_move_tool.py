from mcp.server.fastmcp import FastMCP
from models.file_models import FileMoveIn
from services.file_service import FileService

mcp = FastMCP("smart-file-ops-server")
file_service = FileService()

@mcp.tool(description="Move files from one directory to another.")
async def file_move(source_directory: str, target_directory: str, timeout_sec: int = 60) -> dict:
    _ = FileMoveIn(source_directory=source_directory, target_directory=target_directory, timeout_sec=timeout_sec)  # validation
    res = await file_service.move_files(source_directory, target_directory, timeout_sec)
    return res.model_dump()
