from pydantic import BaseModel
from typing import Optional, Literal

class KeywordSearchRequest(BaseModel):
    query: str
    language: Optional[Literal["english", "french", "simple"]] = "simple"
    limit: Optional[int] = 10

class KeywordSearchResponse(BaseModel):
    document_id: str
    chunk_id: int
    content: str
    rank: float