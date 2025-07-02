from crewai.tools import tool
from app.services.mongodb_tool import MongoDBTool

@tool("Get Outstanding Payments")
def get_outstanding_payments_tool() -> list:
    """
    Useful for listing all orders that currently have a 'pending' status, indicating outstanding payments.
    Returns a list of orders with their ID, client name, course, and amount due.
    """
    # Assume MongoDBTool().get_outstanding_payments returns a list of dictionaries/objects
    # e.g., [{'order_id': 123, 'client_name': 'John Doe', 'course': 'Yoga', 'amount_due': 50.0}]
    return MongoDBTool().get_outstanding_payments()