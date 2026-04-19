from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

user_query = input("HUMAN QUERY:\n")

response = client.responses.create(
    model="gpt-5.2",
    input=[
        {
            "role": "user",
            "content": "hi, my name is aryan."
        },
        {
            "role": "assistant",
            "content": "Hi Aryan — how can I help you today?"
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
)

print("AI RESPONSE:\n")
print(response.output_text)