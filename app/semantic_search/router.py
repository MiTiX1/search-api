from typing import List
from fastapi import APIRouter, status
from .schemas import SemanticSearchRequest, SemanticSearchResponse
from .service import SemanticSearchService

router = APIRouter(prefix="/search")

@router.post("/semantic-search", status_code=status.HTTP_200_OK, response_model=List[SemanticSearchResponse])
async def semantic_search(payload: SemanticSearchRequest):
    return await SemanticSearchService.search(
        query=payload.query,
        limit=payload.limit
    )