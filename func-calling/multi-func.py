from dotenv import load_dotenv
from openai import OpenAI
import requests
import os
import json
import subprocess

# SETUP YOUR ENVIRONMENT
load_dotenv()
client = OpenAI()

f = open("weather_description.txt","r")
function_description = f.read()
f.close()

# FIRST FUNCTION - GET WEATHER
def get_weather(zipcode):
    apikey = os.getenv("OPENWEATHERMAP_API_KEY")
    countrycode = "in"
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={apikey}"
    result = requests.get(url)
    response = result.json()
    return response

# SECOND FUNCTION - GET ORDER STATUS

def get_delivery_date(user_id):
    url = f"http://localhost:8000/delivery/{user_id}"
    result = requests.get(url)
    if result.status_code != 200:
        return {"error": "user not found"}
    return result.json()

# THIRD FUNCTION - RUN COMMAND

def run_shell(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        shell=True
    )
    return result.stdout #stdin, stdout, stderr 

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
    },
    {
        "type": "function",
        "name": "get_delivery_date",
        "description": "Get delivery details for a user including item, delivery date and status",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user (1,2 or 3)"
                }
            },
            "required": ["user_id"],
        }
    },
    {
        "type": "function",
        "name": "run_shell",
        "description": "Run a linux shell command by providing the command and get the output of the command",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The linux shell command to execute."
                }
            },
            "required": ["command"]
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
        elif item.name == "get_delivery_date":
            result = get_delivery_date(args['user_id'])
        elif item.name == "run_shell":
            result = run_shell(args['command'])
            print(result)
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
print(final_response.output_text)