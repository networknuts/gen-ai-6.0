from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.2",
    input="what is the weather in delhi, india today?"
)

print(response.output_text)