import os
from crewai import Agent, Task, Crew, LLM # Import CrewAI's LLM
# Import support-specific tools using their function names
from app.tools.get_order_status_tool import get_order_status_tool
from app.tools.list_upcoming_classes_tool import list_upcoming_classes_tool
from app.tools.filter_classes_tool import filter_classes_tool
from app.tools.get_client_details_tool import get_client_details_tool
from app.tools.get_client_enrolled_services_tool import get_client_enrolled_services_tool
from app.tools.get_order_details_by_client_tool import get_order_details_by_client_tool
from app.tools.get_payment_details_for_order_tool import get_payment_details_for_order_tool
from app.tools.calculate_pending_dues_tool import calculate_pending_dues_tool
from app.tools.create_client_tool import create_client_tool
from app.tools.create_order_tool import create_order_tool

# Import both caching and conversation history functions
from app.cache.redis_cache import get_cached, set_cached, get_conversation_history, add_to_conversation_history
from app.core.config import GEMINI_API_KEY

class SupportAgent:
    def __init__(self):
        direct_llm = LLM(
            model="gemini/gemini-2.5-pro",
            api_key=GEMINI_API_KEY,
        )
    
        self.agent = Agent(
            role="Support Assistant",
            goal=(
                "Handle course, order, payment, and client queries, "
                "and facilitate client and order creation. Always provide clear, concise, and helpful answers."
            ),
            tools=[
                get_order_status_tool,
                list_upcoming_classes_tool,
                filter_classes_tool,
                get_client_details_tool,
                get_client_enrolled_services_tool,
                get_order_details_by_client_tool,
                get_payment_details_for_order_tool,
                calculate_pending_dues_tool,
                create_client_tool,
                create_order_tool,
            ],
            llm=direct_llm, # Pass the CrewAI LLM instance
            verbose=True,
            allow_delegation=False,
            backstory=(
                "You are a helpful AI assistant specialized in managing customer service "
                "queries related to an online learning platform. Your expertise includes "
                "providing information on course/class details, order and payment statuses, "
                "and client information. You are also capable of creating new client records "
                "and processing new orders. Your primary function is to interpret user requests, "
                "use appropriate tools to fetch or create data, and provide accurate responses."
            )
        )

    def run(self, prompt: str, session_id: str = "global"):
        # 1) Check cache for exact prompt match
        if cached_response := get_cached(session_id, prompt):
            print(f"[{session_id}] Cache hit for prompt: '{prompt}'")
            return {"cached": True, "response": cached_response}

        # 2) Retrieve conversation history for context
        conversation_history = get_conversation_history(session_id)
        
        # Format history into a string to prepend to the current prompt
        # The LLM reads this combined string to understand context.
        context_string = ""
        if conversation_history:
            context_string = "Previous conversation:\n" + "\n".join([f"{turn['role'].capitalize()}: {turn['content']}" for turn in conversation_history]) + "\n\n"
        
        # Construct the full input for the agent, including context
        full_prompt_for_agent = f"{context_string}User: {prompt}"

        # 3) Run agent if not cached
        print(f"[{session_id}] Cache miss for prompt: '{prompt}', running agent...")

        task = Task(
            description=full_prompt_for_agent, # Pass the enriched prompt
            agent=self.agent,
            expected_output="A concise and helpful answer relevant to the user's query, considering the conversation history."
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )

        resp = crew.kickoff()

        # 4) Store current turn in conversation history
        # Store both the user's original prompt and the agent's final response
        add_to_conversation_history(session_id, "user", prompt)
        add_to_conversation_history(session_id, "assistant", resp) 

        # 5) Cache result for exact prompt match (still useful for direct repeats)
        set_cached(session_id, prompt, resp)
        print(f"[{session_id}] Agent response cached for prompt: '{prompt}'")
        return {"cached": False, "response": resp}