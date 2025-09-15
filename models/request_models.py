from pydantic import BaseModel
from typing import Optional, List, Dict



class Message(BaseModel):
    role: str
    content: str

class QueryPayload(BaseModel):
    query: str
    history: List[Message] = []

from pydantic import Field

class QueryRequest(BaseModel):
    query: str
    history: List[Dict[str, str]] = Field(default_factory=list)

# class QueryRequest(BaseModel):
#     query: str
#     history: List[Dict[str, str]] = []   # Optional, defaults to empty list
    



class ImageAnalysisRequest(BaseModel):
    image_url: Optional[str] = None
    image_file: Optional[bytes] = None
    image_data: str
    mime_type: str