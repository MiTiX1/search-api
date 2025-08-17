import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.config import GcpConfig
from app.commons.clients import cloud_sql_client

class SemanticSearchService:
    logger = logging.getLogger(__name__)
    _model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    @staticmethod
    async def search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
        query_embedding = str(SemanticSearchService._model.encode(query, normalize_embeddings=True).tolist())
        
        stmt = text(f"""
        SELECT document_id,
               chunk_id,
               content,
               1 - (embedding <#> :query_embedding) AS similarity
        FROM {GcpConfig.CloudSQLConfig.document_chunks_embeddings_table}
        ORDER BY embedding <#> :query_embedding
        LIMIT :limit;
        """)

        async with await cloud_sql_client.get_session() as session:
            try:
                result = await session.execute(
                    stmt,
                    {"query_embedding": query_embedding, "limit": limit}
                )
                rows = result.fetchall()
            except SQLAlchemyError as e:
                SemanticSearchService.logger.error(f"Semantic search failed: {e}")
                raise HTTPException(status_code=500, detail="Semantic search failed")
            except Exception as e:
                SemanticSearchService.logger.error(f"Semantic search failed: {e}")
                raise HTTPException(status_code=500, detail="Semantic search failed")

        return [
            {
                "document_id": row.document_id,
                "chunk_id": row.chunk_id,
                "content": row.content,
                "similarity": float(row.similarity),
            }
            for row in rows
        ]