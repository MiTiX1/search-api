import uvicorn
from fastapi import FastAPI, APIRouter
from .keyword_search import keyword_search_router

app = FastAPI()
api_router = APIRouter(prefix="/api/v1")

@api_router.get("/_health")
def health():
    return {"status": "up"}


api_router.include_router(router=keyword_search_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)