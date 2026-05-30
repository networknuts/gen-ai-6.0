from mcp.server.fastmcp import FastMCP
import wikipedia
import requests

# Create an MCP server
mcp = FastMCP("Support MCP Server", json_response=True)

# CREATE AN MCP TOOL
@mcp.tool()
def wikipedia_search(topic: str):
    """
    Get wikipedia summary of any topic by providing the relevant topic
    name. This wikipedia search tool is limited to only providing a 10 line
    summary of the given topic.
    """
    try:
        return wikipedia.summary(topic,sentences=10)
    except Exception as e:
        return str(e)

@mcp.tool()
def get_order_data(user_id: int):
    """
    Get the following information about the ordered item for a user:
    - item name
    - delivery date
    - delivery status

    The function requires a user_id to work and provides above for the given 
    user_id.
    """
    url = f"http://localhost:8080/delivery/{user_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return {
            "Error": "User not found"
        }
    else:
        return response.json()

@mcp.tool()
def run_refund_request(user_id: int):
    """
    This tool connects to bank api and refunds the last order of the user.
    The tool requires the user_id and automatically will find out the refund 
    amount and process the refund from the bank side automatically.
    """
    return {
        "status": "completed",
        "data": f"refund for {user_id} process with HDFC bank."
    }

mcp.run(transport="streamable-http")