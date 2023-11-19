from psycopg2 import connect
from os import environ
from random import choice
from json import load

connection = connect(
    host=environ["PGHOST"],
    user=environ["PGUSER"],
    password=environ["PGPASSWORD"],
    database="semantic",
)
cursor = connection.cursor()

# Expecting a local file embeddings.json
# see processing/embeddings.py
with open("embeddings.json") as f:
    embeddings = load(f)

random_orgs = ["org1", "org2", "org3", "org4", "org5"]
for each in embeddings:
    each["org_id"] = choice(random_orgs)  # add a random org_id for where clauses
    values = tuple(each.values())
    cursor.execute(
        "INSERT into search(segment, document_id, segment_id, embedding, org_id) VALUES (%s, %s, %s, %s, %s)",
        values,
    )

connection.commit()
connection.close()
