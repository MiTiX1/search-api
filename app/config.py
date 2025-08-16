from dotenv import load_dotenv
load_dotenv() # nopep8

import os

class GcpConfig:
    class CloudSQLConfig:
        instance_connection_name = os.environ.get("INSTANCE_CONNECTION_NAME")
        db_user = os.environ.get("DB_USER")
        db_password = os.environ.get("DB_PASSWORD")
        db_name = os.environ.get("DB_NAME")

        document_chunks_table = os.environ.get("DOCUMENT_CHUNKS_TABLE", "document_chunks")
        document_chunks_embeddings_table = os.environ.get("DOCUMENT_CHUNKS_EMBEDDINGS_TABLE", "document_chunks_embeddings")