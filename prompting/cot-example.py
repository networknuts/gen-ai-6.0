from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

f = open("cot.txt","r")
SYSTEM_PROMPT = f.read()
f.close()

user_query = input("Human Query: ")

response = client.responses.create(
    model="gpt-5.2",
    instructions=SYSTEM_PROMPT,
    input=user_query
)

print("AI Response:\n")
print(response.output_text)