from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

# The @tool decorator makes this function directly usable as a CrewAI tool.
# The docstring becomes the tool's description.
# Type hints for arguments are crucial for the agent to understand how to use the tool.
@tool("Get Order Status")
def get_order_status_tool(order_id: int) -> str:
    """
    Useful for fetching the current status of an order by its numerical ID 
    (e.g., 'Has order #12345 been paid?'). 
    Returns the status (e.g., 'pending', 'paid', or 'not found').
    """
    # Replace with your actual MongoDBTool call
    return MongoDBTool().get_order_status(order_id)

# You would then import get_order_status_tool in your agent
# and add it directly to the tools list:
# tools=[get_order_status_tool]