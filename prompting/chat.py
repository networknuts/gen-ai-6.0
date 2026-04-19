from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

user_query = input("HUMAN QUERY:\n")

response = client.responses.create(
    model="gpt-5.2",
    input=user_query
)

print("AI RESPONSE:\n")
print(response.output_text)