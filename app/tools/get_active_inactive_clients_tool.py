from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Active and Inactive Clients Count")
def get_active_inactive_clients_count_tool() -> dict:
    """
    Useful for counting the total number of active and inactive clients in the system.
    Returns a dictionary with counts for both active and inactive categories.
    """
    # Assume MongoDBTool().get_active_inactive_clients_count returns a dictionary like {'active': X, 'inactive': Y}
    return MongoDBTool().get_active_inactive_clients_count()