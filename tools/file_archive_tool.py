from mcp.server.fastmcp import FastMCP
from models.file_models import FileArchiveIn
from services.file_service import FileService

mcp = FastMCP("smart-file-ops-server")
file_service = FileService()

@mcp.tool(description="Create an archive (ZIP) from the specified directory.")
async def file_archive(directory: str, archive_name: str, timeout_sec: int = 60) -> dict:
    _ = FileArchiveIn(directory=directory, archive_name=archive_name, timeout_sec=timeout_sec)  # validation
    res = await file_service.create_archive(directory, archive_name, timeout_sec)
    return res.model_dump()
