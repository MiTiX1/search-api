from pydantic import BaseModel

class KeywordSearchRequest(BaseModel):
    query: str

class KeywordSearchResponse(BaseModel):
    text: str