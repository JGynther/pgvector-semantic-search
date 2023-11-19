# Vector search

Using PostgreSQL with [pgvector](https://github.com/pgvector/pgvector) for efficient semantic search over transcripts.

The solution consist of multiple pieces

- Processing
- Database setup
- API using FastAPI
- Considerations and performance
- Future possibilities

## Processing

`processing/`

Example process of converting meeting transcripts first into small (~200 tokens), overlapping segments and then into embeddings.

After being converted to embeddings the files take up less than 50 % of the space of full transcripts fully segmented and less than 2 % without segmenting.

There are 2 reasons for segmenting documents:

1. Embedding models have a maximum token size per input
2. With segmented documents it's not only possible to find most relevant document as per user's query, but exactly which sections of that document are relevant

The reason for overlapping documents, while taking more resources (compute, storage) lowers the chance of an imporant sentence or part getting cut from surrounding context.

The embeddings use Cohere's `Cohere-embed-multilingual-v3.0` for generating embeddings. It can be either [self-hosted](https://aws.amazon.com/marketplace/pp/prodview-z6huxszcqc25i) on SageMaker or used through Amazon Bedrock. The example pipeline uses Bedrock.

Other multilingual embedding models should also be considered, as reducing dimensionality of vectors increases [pgvector's performance](https://supabase.com/blog/fewer-dimensions-are-better-pgvector).

The pipeline is not production ready as making it sensible depends heavily on the prior process. Embedding new transcripts is likely best done in the same pipeline as they are transcribed. For development purposes processing results are saved to `json` files.

While the full documents can't be embedded as is, we can use simple vector math to combine all segments for the full document. Please see `future/` for more.

## Database setup

`sql/`

Example of activating pgvector and creating an embedding table is provided. Setup was tested on a `RDS Aurora PostgreSQL 15.3` database hosted on a `db.t4g.medium` instance.

```sql
-- Schema
org_id          TEXT
document_id     TEXT
segment_id      INTEGER
segment         TEXT
embedding       VECTOR(1024)
PRIMARY KEY (org_id, document_id, segment_id)
```

Table schema contains a reference to the original document (document_id), text of the actual segment (segment) and the 1024-dimensional embedding (embedding). In addition a "group identifier" called "org_id" here is used as a boundary for which transcripts user has access to.

In order to use vector similarity to rank results you only need to use a `ORDER BY` clause with new operators provided by pgvector (<->, <=>).

```sql
-- Not a real embedding for brevity
-- <=> for cosine similarity
SELECT document_id, segment_id, segment, embedding <=> '[1,2,3]' AS distance
FROM search
WHERE org_id = 'org1'
ORDER BY embedding <=> '[1,2,3]'
LIMIT 5;
```

`sql/batch_load.py` also showcases inserting the `embedding.json` created with the processing pipeline into the database.

## API using FastAPI

`api/`

Simple FastAPI api is used to interface with database and embedding model and serve search queries under one endpoint. The endpoint at `/search` expects search query as a url parameter like `/search?query=example`.

In addition there is a simple interface to Amazon Bedrock for the embedding model and Postgres database.

`Dockerfile` provides a minimal environment for containeraizing the API. Docker Compose file also exists, but will not work out of the box. Default Postgres image lacks pgvector.

## Considerations and performance

`tests/`

A very naive load test is available under tests. The test is single threaded and consists of 576 requests to the search API. Query speed is not tied to database performance (<10 % DBLoad at all times) but rather latency of the embedding process, which is a network bound call. The following test was done against real infrastructure.

> Processed 576 queries in 135.587 seconds.
>
> ~4.248 queries per second.

The search API could be scaled horizontally for more performance. Pgvector also supports creating
indexes on vectors which could be used to boost database performance.

### Quality

For an example query of "last weeks sales meeting" we get the following segment:

> of her district uhuh mhm. uh okay anybody here w- wanna play Jay? anybody here from the Florida sales team? anyone? okay. go ahead, Brenda, you're having a conversation with Jay. you gotta get\_ you have a plan of action go ahead. you have some ideas let's see the follow-through. um, so Jay how do you, keep your sales uh ten percent above the prime, throughout the year? good teamwork we work together, c'mon Jay, you know, um, i don't know you know we uh, we cover for each other we make sure we get on each other's uh butts per se and you know, make sure everyone's getting the job done, help each other out you don't think i'm gonna sell you out do you? sell us out to who? i don't i don't understand what you're saying. (hey,

Which is definitely a meeting about sales. In fact 4 / 5 top results reference the same original document, which at least passes a sanity check quality wise.

## Future

In addition to segments of documents that can be used to find specific parts of a document that respond to a search query, we can "reconstruct" the embedding of the whole document by combining the vectors of its segments.

This would trivially with neligible compute for us to also rank documents in relation to each other (think which meetings are most similar to this one).

```sql
WITH target_embedding AS (
    SELECT embedding
    FROM documents
    WHERE document_id = 'randomidhere'
)

SELECT document_id
FROM documents
ORDER BY embedding <=> target_embedding
LIMIT 5;
```
