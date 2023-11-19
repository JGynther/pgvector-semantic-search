from transformers import AutoTokenizer
from segment import segment
import boto3
import json

with open("transcripts.json") as f:
    transcripts = json.load(f)

model = "Cohere/Cohere-embed-multilingual-v3.0"
tokenizer = AutoTokenizer.from_pretrained(model)

segmented_transcripts = []

for transcript in transcripts:
    text = transcript["text"]
    segments = segment(text, tokenizer)
    for i, each in enumerate(segments):
        obj = {"text": each, "document_id": transcript["id"], "id": i}
        segmented_transcripts.append(obj)


bedrock = boto3.client("bedrock-runtime", "us-east-1")
args = {
    "modelId": "cohere.embed-multilingual-v3",
    "accept": "application/json",
    "contentType": "application/json",
}


for segmented in segmented_transcripts:
    payload = json.dumps(
        {
            "texts": [segmented["text"]],
            "input_type": "search_document",
            "truncate": "NONE",
        }
    )

    response = bedrock.invoke_model(body=payload, **args)
    body = json.loads(response["body"].read())

    segmented["embedding"] = body["embeddings"][0]


with open("embeddings.json", "w") as f:
    json.dump(segmented_transcripts, f)
