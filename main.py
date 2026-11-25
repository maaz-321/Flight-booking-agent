import os
from groq import Groq
from dotenv import load_dotenv

# Import the agent class, tool functions registry, and JSON tool schemas from src
from src.agent import FlightBookingAgent
from src.tools import TOOL_REGISTRY
from src.schemas import FLIGHT_TOOLS_SCHEMA

# Load secret environment variables (like GROQ_API_KEY) from the .env file
load_dotenv()

# Define the behavior, rules, and personality of the AI assistant
SYSTEM_PROMPT = """
You are 'SkyBot', a helpful and polite Flight Booking Assistant.
- Always search for flights first when a user asks about travel options.
- Before calling `book_flight`, make sure you know both the exact `flight_no` and the `passenger_name`. If the passenger's name is missing, politely ask for it first.
- Always show the PNR number clearly after a successful booking.
"""


def main():
    # Read the Groq API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file!")

    # Initialize the Groq API client
    client = Groq(api_key=api_key)

    # Create the FlightBookingAgent instance with its brain, rules, and tools
    agent = FlightBookingAgent(
        client=client,
        model="llama-3.3-70b-versatile",
        system=SYSTEM_PROMPT,
        tools=FLIGHT_TOOLS_SCHEMA,
        registry=TOOL_REGISTRY
    )

    print("SkyBot Flight Agent Ready! (Type 'exit' to quit)\n")

    # Start an interactive terminal chat loop
    while True:
        # Get user input from the terminal and remove extra spaces
        user_input = input("You: ").strip()

        # Stop the program if the user types 'exit' or 'quit'
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Have a safe flight. ✈️")
            break

        # Skip empty messages if the user just pressed Enter
        if not user_input:
            continue

        # Pass the user's message to the agent (triggers __call__ -> execute) and print the reply
        reply = agent(user_input)
        print(f"SkyBot: {reply}\n")


# Run the main() function only when this file is executed directly
if __name__ == "__main__":
    main()