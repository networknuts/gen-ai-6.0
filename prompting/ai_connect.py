import requests 
import json

API_KEY = "sensitive value"

AI_URL = "https://api.openai.com/v1/responses"

HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

DATA = {
    "model": "gpt-5.4",
    "input": "what is the capital of USA?"
}

result = requests.post(AI_URL,data=json.dumps(DATA),headers=HEADERS)

print(result.json())