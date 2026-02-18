from __future__ import annotations

import asyncio
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from services.file_service import FileService
from models.file_models import FileMoveIn, FileRenameIn, FileScanIn, FileArchiveIn
from settings import build_settings, get_default_env_path
from utils.validate import validate_directory
from models.result import ToolResult, ErrorInfo

env_path = get_default_env_path()
load_dotenv(dotenv_path=env_path, override=False)

settings = build_settings()

mcp = FastMCP("smart-file-ops-server")

file_service = FileService(settings=settings)


@mcp.tool(description=""" 
Scan a directory and return a list of files along with metadata (e.g., size, date modified).
Use when:
- You need to get an overview of the contents of a directory.
- You need to identify specific file types or properties.

Inputs:
- directory: path to the directory to scan
- timeout_sec: maximum time for scanning operation (seconds)

Returns (ToolResult):
- ok=true: data contains list of file metadata (filename, size, last modified, etc.)
- ok=false: error.code/message and details
""")
async def file_scan(directory: str, timeout_sec: int = 60) -> dict:
    _ = FileScanIn(directory=directory, timeout_sec=timeout_sec)  # validation
    res = await asyncio.to_thread(file_service.scan_directory, directory, timeout_sec)
    return res


@mcp.tool(description=""" 
Rename files in a directory based on a provided naming convention.

Use when:
- You want to apply a consistent naming scheme across files.
- You want to rename files based on metadata or content.

Inputs:
- directory: path to the directory where files are located
- naming_scheme: a rule or pattern to rename files (e.g., "year-month-day_originalname")
- timeout_sec: maximum time for renaming operation (seconds)

Returns (ToolResult):
- ok=true: data contains renamed files and success message
- ok=false: error.code/message and details
""")
async def file_rename(directory: str, naming_scheme: str, timeout_sec: int = 60) -> dict:
    _ = FileRenameIn(directory=directory, naming_scheme=naming_scheme, timeout_sec=timeout_sec)  # validation
    res = await asyncio.to_thread(file_service.rename_files, directory, naming_scheme, timeout_sec)
    return res


@mcp.tool(description=""" 
Move files from one directory to another.

Use when:
- You want to reorganize files into different directories.
- You want to consolidate files of a certain type.

Inputs:
- source_directory: path to the directory from which files will be moved
- target_directory: path to the destination directory
- timeout_sec: maximum time for move operation (seconds)

Returns (ToolResult):
- ok=true: data contains move details (source, target, list of files moved)
- ok=false: error.code/message and details
""")
async def file_move(source_directory: str, target_directory: str, timeout_sec: int = 60) -> dict:
    _ = FileMoveIn(source_directory=source_directory, target_directory=target_directory, timeout_sec=timeout_sec)  # validation
    res = await asyncio.to_thread(file_service.move_files, source_directory, target_directory, timeout_sec)
    return res


@mcp.tool(description=""" 
Create an archive (ZIP) from the specified directory and its contents.

Use when:
- You need to compress files for storage or transport.
- You want to group related files into a single archive.

Inputs:
- directory: path to the directory to compress
- archive_name: desired name for the archive
- timeout_sec: maximum time for archiving operation (seconds)

Returns (ToolResult):
- ok=true: data contains archive details (archive name, location)
- ok=false: error.code/message and details
""")
async def file_archive(directory: str, archive_name: str, timeout_sec: int = 60) -> dict:
    _ = FileArchiveIn(directory=directory, archive_name=archive_name, timeout_sec=timeout_sec)  # validation
    res = await asyncio.to_thread(file_service.create_archive, directory, archive_name, timeout_sec)
    return res


def __validate_directory(directory: str) -> dict:
    ok, directory_abs = validate_directory(directory)
    if not ok:
        return ToolResult(
            ok=False,
            error=ErrorInfo(
                code=1, 
                message="Not a valid directory.",
                details={"directory": directory_abs}
            )
        ).model_dump()
    return {"ok": True, "directory_abs": directory_abs}


if __name__ == "__main__":
    mcp.run()
