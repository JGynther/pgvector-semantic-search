-- create table
CREATE TABLE documents (
    document_id PRIMARY KEY TEXT,
    text TEXT,
    embedding VECTOR(1024),
);