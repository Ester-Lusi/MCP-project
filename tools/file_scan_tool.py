from mcp.server.fastmcp import FastMCP
from models.file_models import FileScanIn
from services.file_service import FileService

mcp = FastMCP("smart-file-ops-server")
file_service = FileService()

@mcp.tool(description="Scan a directory and return a list of files along with metadata.")
async def file_scan(directory: str, timeout_sec: int = 60) -> dict:
    _ = FileScanIn(directory=directory, timeout_sec=timeout_sec)  # validation
    res = await file_service.scan_directory(directory, timeout_sec)
    return res.model_dump()
