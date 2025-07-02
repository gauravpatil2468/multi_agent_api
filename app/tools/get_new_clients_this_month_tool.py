from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get New Clients This Month")
def get_new_clients_this_month_tool() -> int:
    """
    Useful for counting how many new clients have registered in the current month.
    Returns the number of new clients registered this month as an integer.
    """
    # Assume MongoDBTool().get_new_clients_this_month returns an integer count
    return MongoDBTool().get_new_clients_this_month()