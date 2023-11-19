-- Not a real embedding for brevity
-- <=> for cosine similarity
SELECT document_id, segment_id, segment, embedding <=> '[1,2,3]' AS distance
FROM search
WHERE org_id = 'org1'
ORDER BY embedding <=> '[1,2,3]'
LIMIT 5;