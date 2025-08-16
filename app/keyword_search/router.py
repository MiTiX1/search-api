from fastapi import APIRouter, status
from .schemas import KeywordSearchRequest, KeywordSearchResponse

router = APIRouter(prefix="/search")

@router.post("/keyword-search", status_code=status.HTTP_200_OK, response_model=KeywordSearchResponse)
async def keyword_search(payload: KeywordSearchRequest):
    return KeywordSearchResponse(
        text="it worked"
    )