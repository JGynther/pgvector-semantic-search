from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.psql import create_db_connection, pgvector_search
from app.bedrock import encode


api = FastAPI()
cursor = create_db_connection()


@api.get("/search")
def search(query: str):
    embedding = encode(query)
    results = pgvector_search(embedding, cursor)
    return JSONResponse(results)
