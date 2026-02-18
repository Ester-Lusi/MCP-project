from pydantic import BaseModel
from typing import Optional, Any

# ErrorInfo class will hold error details like code, message, and additional details
class ErrorInfo(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None

# ToolResult class to represent the result of a tool's execution
class ToolResult(BaseModel):
    ok: bool
    data: Optional[Any] = None
    error: Optional[ErrorInfo] = None

    def model_dump(self):
        """
        Method to dump the data as a dictionary (or json-like format).
        This is useful for returning responses.
        """
        return self.dict()

