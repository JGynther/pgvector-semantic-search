-- enable pgvector on database
CREATE extension vector;

-- create table
CREATE TABLE search (
    org_id TEXT,
    document_id TEXT,
    segment_id INTEGER,
    segment TEXT,
    embedding VECTOR(1024),
    PRIMARY KEY(org_id, document_id, segment_id)
);