from pydantic import BaseModel

class FileScanIn(BaseModel):
    directory: str
    timeout_sec: int

class FileRenameIn(BaseModel):
    directory: str
    naming_scheme: str
    timeout_sec: int

class FileMoveIn(BaseModel):
    source_directory: str
    target_directory: str
    timeout_sec: int

class FileArchiveIn(BaseModel):
    directory: str
    archive_name: str
    timeout_sec: int
