from pydantic import BaseModel
from typing import Optional, Literal

class SemanticSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

class SemanticSearchResponse(BaseModel):
    document_id: str
    chunk_id: int
    content: str
    similarity: float