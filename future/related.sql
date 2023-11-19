WITH target_embedding AS (
    SELECT embedding
    FROM documents
    WHERE document_id = ?
)

SELECT document_id
FROM documents
ORDER BY embedding <=> target_embedding
LIMIT 5;