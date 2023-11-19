from os import environ
from psycopg2 import connect


def create_db_connection():
    connection = connect(
        host=environ["PGHOST"],
        user=environ["PGUSER"],
        password=environ["PGPASSWORD"],
        database="semantic",
    )

    return connection.cursor()


def pgvector_search(embedding: list[float], cursor):
    guard_clause = "WHERE org_id = 'org3'"

    sql = f"""
        SELECT  org_id, 
                document_id, 
                segment_id, 
                segment, 
                embedding <=> '{embedding}' AS distance 
        FROM search 
        {guard_clause} 
        ORDER BY embedding <=> '{embedding}' 
        LIMIT 5
    """

    cursor.execute(sql)
    results = cursor.fetchall()

    return [
        {
            "org_id": each[0],
            "document_id": each[1],
            "segment_id": each[2],
            "segment": each[3],
            "distance": each[4],
        }
        for each in results
    ]
