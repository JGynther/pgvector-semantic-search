import boto3
import json

bedrock = boto3.client("bedrock-runtime", "us-east-1")

args = {
    "modelId": "cohere.embed-multilingual-v3",
    "accept": "application/json",
    "contentType": "application/json",
}


def encode(prompt: str) -> list[float]:
    payload = json.dumps(
        {
            "texts": [prompt],
            "input_type": "search_query",
            "truncate": "RIGHT",  # User inputs might be too long
        }
    )

    response = bedrock.invoke_model(body=payload, **args)
    body = json.loads(response["body"].read())

    return body["embeddings"][0]
