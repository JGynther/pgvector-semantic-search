from time import time
from random import shuffle
import requests

random_queries = [
    "Find the meeting where we discussed launching the new product",
    "Show me the minutes from the April 15th leadership meeting",
    "Which meeting set the June 30th deadline for the proposal?",
    "Who was responsible for following up on the marketing plan?",
    "Did we make a decision on the Colorado office space?",
    "Bring up all discussions about improving customer service",
    "Show me meetings from last quarter that mentioned budget issues",
    "Search transcripts for meetings with Susan Johnson",
    "Find meetings where the software demo didn't go as planned",
    "Any meetings talk about hiring additional developers?",
    "Pull up conversations about progress on the Big Client project",
    "Show action items assigned to me from last month",
    "Find discussions on proposals we submitted in May",
    "Search for meetings Jones from Sales attended",
    "Bring up past meetings addressing low employee morale",
    "Which meeting outlined the Q3 goals and objectives",
    "Find mentions of the new product launch",
    "Anything discussed about marketing budget",
    "What was said about deadlines for the quarterly report",
    "Notes from our brainstorming session last week",
    "Show me where we talked about hiring a new sales rep",
    "Transcript sections related to customer feedback",
    "Find the action items from our last meeting",
    "Search for discussions on improving customer service",
    "Show me mentions of the competition's new features",
    "Transcript parts about increasing website traffic",
    "Find mentions of Bob's presentation on data analytics",
    "Search for conversations around expanding to new markets",
    "Highlight discussions on improving office efficiency",
    "Transcribe parts where we debated new partnership opportunities",
    "Find the timeline we set for the software rollout",
    "Search for chat on promoting team building activities",
    "Transcribe sections about updates to our recruiting process",
    "Show me discussions on adding new benefits for employees",
    "Transcript segments on scheduling more client meetings",
    "Find mentions of changes to our social media strategy",
]

for i, each in enumerate(random_queries):
    random_queries[i] = each.replace(" ", "%20")

random_queries += random_queries
random_queries += random_queries
random_queries += random_queries
random_queries += random_queries

shuffle(random_queries)

# Start test
start = time()

for query in random_queries:
    response = requests.get(f"http://127.0.0.1:8000/search?query={query}")

end = time()

print(f"Processed {len(random_queries)} queries in {end-start} seconds")
print(f"~{len(random_queries) / (end-start)} queries per second")
