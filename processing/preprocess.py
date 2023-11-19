from os import listdir
import json

transcripts = []

# transcript jsons expected in local folder "transcripts"
for file in listdir("transcripts"):
    with open(f"transcripts/{file}") as f:
        json_content = json.load(f)
        text_content = json_content["results"]["transcripts"][0]["transcript"]
        transcripts.append({"id": file[:-5], "text": text_content})

with open("transcripts.json", "w") as f:
    json.dump(transcripts, f)
