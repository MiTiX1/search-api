from typing import List
from fastapi import APIRouter, status
from .schemas import KeywordSearchRequest, KeywordSearchResponse
from .service import KeywordSearchService

router = APIRouter()

@router.post("/keyword-search", status_code=status.HTTP_200_OK, response_model=List[KeywordSearchResponse])
async def keyword_search(payload: KeywordSearchRequest):
    return await KeywordSearchService.search(
        query=payload.query,
        language=payload.language,
        limit=payload.limit
    )