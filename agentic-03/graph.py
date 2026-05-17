from dotenv import load_dotenv
from langgraph.graph import StateGraph, END 
from langchain_openai import ChatOpenAI 
from typing import TypedDict 
import json
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient

# SETUP THE ENVIRONMENT
load_dotenv()

llm_developer = ChatOpenAI(
    model="gpt-5.4-nano"
)

llm_qa = ChatOpenAI(
    model="gpt-5.4"
)

MONGO_DB = "mongodb://localhost:27017"
client = MongoClient(MONGO_DB)

MAX_RETRIES = 3 

def llm_json(prompt):
    response = llm_qa.invoke(
        "Return only valid json. no markdown.\n" + prompt
    ).content.strip()
    return json.loads(response)

# DEFINE OUR STATE

class CodeState(TypedDict):
    user_request: str 
    code: str
    rating: int 
    feedback: str 
    retries: int 
    status: str 

# NODE 1: DEVELOPER AGENT

def developer_agent(state: CodeState):
    prompt = f"""
You are a nodejs developer. Write the code for app as per the request of the user:
{state['user_request']}

If feedback is provided, improve the previous version of the code.
Previous code:
{state['code']}

Feedback:
{state['feedback']}

RETURN ONLY THE FULL NODEJS CODE.
    """
    result = llm_developer.invoke(prompt).content
    return {
        "code": result,
        "feedback": ""
    }

# NODE 2: QA AGENT NODE

def qa_agent(state: CodeState):
    prompt = f"""
You are a strict NODEJS QA Engineer.
Evaluate the following NODEJS code for the given requirements:
- correctness of the code
- structure of the code
- readability of the code
- whether the code is following best production practices
- error handling capabilities of the code
- scalability factor in the code 

Return output in the following JSON format:
{{
    "rating": integer value between 1-10,
    "feedback": "clear explanation of the improvements to make"
}}

Code:
{state['code']}
"""
    result = llm_json(prompt)
    return {
        "rating": int(result['rating']),
        "feedback": result['feedback']
    }

# NODE: APPROVE CODE
def set_approved(state: CodeState):
    return {"status": "approved"}

# NODE: FAILED CODE
def set_failed(state: CodeState):
    return {"status": "failed"}

# INCREMENTAL RETRY LOGIC
def increment_retry(state: CodeState):
    return {"retries": state['retries']+1}

# ROUTER NODE

def check_rating(state: CodeState):
    if state['rating'] >= 7:
        return "approved"
    if state['retries'] >= MAX_RETRIES:
        return "failed"
    return "retry"


# BUILD THE GRAPH

graph = StateGraph(CodeState)

graph.add_node("developer",developer_agent)
graph.add_node("qa",qa_agent)
graph.add_node("approved_node", set_approved)
graph.add_node("failed_node", set_failed)
graph.add_node("retry_increment", increment_retry)

graph.set_entry_point("developer")
graph.add_edge("developer","qa")
graph.add_conditional_edges(
    "qa",
    check_rating,
    {
        "approved": "approved_node",
        "failed": "failed_node",
        "retry": "retry_increment"
    }
)
graph.add_edge("retry_increment","developer")
graph.add_edge("approved_node",END)
graph.add_edge("failed_node", END)

# ADD MONGODB CHECKPOINTING

mongodb_checkpointer = MongoDBSaver(client)

app = graph.compile(checkpointer=mongodb_checkpointer)

user_id = "1" 
thread_id = "2"

# CHECK IF EXISTING THREAD ALREADY EXISTS IN MONGODB

existing = mongodb_checkpointer.get({"configurable": {"thread_id": thread_id, "user_id": user_id}})

try:
    if existing:
        print("RESUMING FROM CHECKPOINT")
        result = app.invoke({},config={"configurable": {"thread_id": thread_id, "user_id": user_id}})
    else:
        user_input = input("Enter NodeJS app to build: ")
        result = app.invoke({
            "user_request": user_input,
            "code": "",
            "rating": 0,
            "feedback": "",
            "retries": 0,
            "status": "running"
        },
        config={"configurable": {"thread_id": thread_id, "user_id": user_id}})

    print("FINAL RESULT")
    print(f"Status: {result['status']}")
    print(f"Final Rating: {result['rating']}")
    print(f"Retries Consumed: {result['retries']}")
    print(f"Feedback: {result['feedback']}")
except Exception as e:
    print(f"Error: {e}")