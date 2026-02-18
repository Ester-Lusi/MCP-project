from mcp.server.fastmcp import FastMCP
from models.file_models import FileRenameIn
from services.file_service import FileService

mcp = FastMCP("smart-file-ops-server")
file_service = FileService()

@mcp.tool(description="Rename files in a directory based on a naming convention.")
async def file_rename(directory: str, naming_scheme: str, timeout_sec: int = 60) -> dict:
    _ = FileRenameIn(directory=directory, naming_scheme=naming_scheme, timeout_sec=timeout_sec)  # validation
    res = await file_service.rename_files(directory, naming_scheme, timeout_sec)
    return res.model_dump()
