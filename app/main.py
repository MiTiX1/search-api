import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from .keyword_search import keyword_search_router
from .semantic_search import semantic_search_router
from .commons.clients import cloud_sql_client
from .config import GcpConfig

@asynccontextmanager
async def lifespan(app: FastAPI):
    await cloud_sql_client.init(
        instance_connection_name=GcpConfig.CloudSQLConfig.instance_connection_name,
        user=GcpConfig.CloudSQLConfig.db_user,
        password=GcpConfig.CloudSQLConfig.db_password,
        db=GcpConfig.CloudSQLConfig.db_name
    )

    await cloud_sql_client.test_connection()

    yield

    await cloud_sql_client.close()

app = FastAPI(lifespan=lifespan)
api_router = APIRouter(prefix="/api/v1")

@api_router.get("/_health")
def health():
    return {"status": "up"}

api_router.include_router(router=keyword_search_router)
api_router.include_router(router=semantic_search_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)