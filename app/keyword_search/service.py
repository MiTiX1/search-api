import logging
from typing import Any, List, Dict
from app.commons.clients import cloud_sql_client
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.config import GcpConfig

class KeywordSearchService:
    logger = logging.getLogger(__name__)

    @staticmethod
    async def search(query: str, language: str = "simple", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Perform a keyword search across document chunks using PostgreSQL full-text search.

        Args:
            query (str): The search term (plain text, converted to tsquery).
            language (str): The text search configuration / language to use. Defaults to 'simple'.
            limit (int): Maximum number of results to return. Defaults to 10.

        Returns:
            List[KeywordSearchResponse]: A list of dictionaries containing:
                - document_id (str)
                - chunk_id (int)
                - content (str)
                - rank (float)

        Raises:
            HTTPException: If the search fails due to a database error.
        """

        stmt = text(f"""
        SELECT document_id,
               chunk_id,
               content,
               ts_rank(tsv, plainto_tsquery('{language}', :query)) AS rank
        FROM {GcpConfig.CloudSQLConfig.document_chunks_table}
        WHERE tsv @@ plainto_tsquery('{language}', :query)
        ORDER BY rank DESC
        LIMIT :limit;
        """)

        async with await cloud_sql_client.get_session() as session:
            try:
                result = await session.execute(stmt, {"query": query, "limit": limit})
                rows = result.fetchall()
            except SQLAlchemyError as e:
                KeywordSearchService.logger.error(f"Keyword search failed: {e}")
                raise HTTPException(status_code=500, detail="Keyword search failed")
            except Exception as e:
                KeywordSearchService.logger.error(f"Keyword search failed: {e}")
                raise HTTPException(status_code=500, detail="Keyword search failed")

        return [
            {
                "document_id": row.document_id,
                "chunk_id": row.chunk_id,
                "content": row.content,
                "rank": float(row.rank),
            }
            for row in rows
        ]