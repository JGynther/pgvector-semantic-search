import json

with open("embeddings.json") as f:
    embeddings = json.load(f)

documents = []

for each in embeddings:
    if each["id"] == 0:
        document = {"document_id": each["document_id"], "embedding": each["embedding"]}
        documents.append(document)
        continue

    current = documents[-1]
    current_embed = current["embedding"]
    embed = each["embedding"]

    new_vector = []

    for i in range(len(embed)):
        _sum = current_embed[i] + embed[i]
        new_vector.append(_sum / 2)

    current["embedding"] = new_vector

with open("documents.json", "w") as f:
    json.dump(documents, f)
