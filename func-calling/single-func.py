from dotenv import load_dotenv
from openai import OpenAI
import requests
import os
import json

# SETUP YOUR ENVIRONMENT
load_dotenv()
client = OpenAI()

f = open("weather_description.txt","r")
function_description = f.read()
f.close()

# CREATE YOUR FUNCTION
def get_weather(zipcode):
    apikey = os.getenv("OPENWEATHERMAP_API_KEY")
    countrycode = "in"
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={apikey}"
    result = requests.get(url)
    response = result.json()
    return response

# TOOL SCHEMA 

openai_tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": function_description,
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "the zip code of the location you want to get the weather information of."
                },
            },
            "required": ["zipcode"],
        }
    }
]


user_query = input("HUMAN QUERY: ")

# FIRST LLM CALL

response = client.responses.create(
    model="gpt-5.4-mini",
    input=user_query,
    tools=openai_tools
)

function_output = []

for item in response.output:
    #print(item)
    if item.type == "function_call":
        args = json.loads(item.arguments)
        if item.name == "get_weather":
            result = get_weather(args['zipcode'])
            print("RAW FUNCTION OUTPUT")
            print(result)
            print("----------------")
        else:
            result = "Unknown function called"
        
        function_output.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps({"result": result})
        })

# SECOND LLM CALL

final_response = client.responses.create(
    model="gpt-5.4-mini",
    input=function_output,
    previous_response_id=response.id
)
print("\n")
print("AI SUMMARIZED FUNCTION OUTPUT:\n")
print(final_response.output_text)