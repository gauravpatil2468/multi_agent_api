from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Client Details")
def get_client_details_tool(query: str) -> dict | None:
    """
    Useful for searching for a client by their name, email, or phone number.
    The input should be the client's name, email, or phone number to search for
    (e.g., 'Priya Sharma', 'priya@example.com', '9999999999').
    Returns the client's basic information (name, email, phone, status, enrolled services) if found,
    otherwise returns None or an empty dictionary.
    """
    # Assume MongoDBTool().get_client returns a dictionary of client details or None if not found
    return MongoDBTool().get_client(query)