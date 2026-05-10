from dotenv import load_dotenv
from langgraph.graph import StateGraph, END 
from langchain_openai import ChatOpenAI 
from typing import TypedDict 

# SETUP THE ENVIRONMENT
load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.4-nano"
)

# DEFINE OUR STATE

class SupportState(TypedDict):
    user_query: str
    intent: str
    response: str 


# DEFINE AGENT / NODE 1: INTENT CLASSIFIER 
def classify_intent(state: SupportState):
    prompt = f"""
    Classify the user query into one of these 3 categories:
    - password_reset
    - order_tracking
    - refund

    Only return the category name 

    User Query: {state['user_query']}
    """
    result = llm.invoke(prompt)
    return {
        "intent": result.content.strip().lower()
    }

# NODE 2: PASSWORD RESET NODE

def handle_password(state: SupportState):
    return {
        "response": (
            "To reset your password, please click on forget password on the login page"
        )
    }

# NODE 3: ORDER TRACKING NODE

def handle_order(state: SupportState):
    return {
        "response": (
            "To track your order, please click on my orders from under your profile."
        )
    }

# NODE 4: REFUND RELATED NODE

def handle_refund(state: SupportState):
    return {
        "response": (
            "We have submitted your refund request to the finance department."
        )
    }

# ROUTER NODE

def route_intent(state: SupportState):
    if state['intent'] == 'password_reset':
        return 'password_node'
    elif state['intent'] == 'order_tracking':
        return 'order_node'
    elif state['intent'] == 'refund':
        return 'refund_node'
    else:
        END 

# BUILDING THE WORKFLOW

graph = StateGraph(SupportState)

graph.add_node("classifier", classify_intent)
graph.add_node("order_node", handle_order)
graph.add_node("password_node", handle_password)
graph.add_node("refund_node", handle_refund)

graph.set_entry_point("classifier")

graph.add_conditional_edges(
    "classifier",
    route_intent
)
graph.add_edge("password_node",END)
graph.add_edge("order_node", END)
graph.add_edge("refund_node", END)

app = graph.compile()

user_input = input("Customer Query: ")

result = app.invoke({
    "user_query": user_input,
    "intent": "",
    "response": ""
})

print(result['intent'])
print(result['response'])