from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.2",
    input="what is the process to make a cup of tea?"
)

print(response.output_text)