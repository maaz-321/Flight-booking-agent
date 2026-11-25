import json
from groq import Groq


class FlightBookingAgent:
    def __init__(self, client: Groq, model: str, system: str, tools: list, registry: dict) -> None:
        # Store the Groq API client connection
        self.client = client
        # Store the name of the LLM model (e.g., llama-3.3-70b-versatile)
        self.model = model
        # Initialize conversation memory with the system instructions
        self.messages: list = [{"role": "system", "content": system}]
        # Store the JSON schemas (tool descriptions) for the LLM
        self.tools = tools
        # Store the dictionary mapping tool names to actual Python functions
        self.registry = registry

    # REQUEST HANDLER: Entry point when calling the agent like a function
    def __call__(self, user_message: str) -> str:
        # Save the user's new message into conversation memory
        self.messages.append({"role": "user", "content": user_message})
        
        # Run the agent executor loop to think, use tools, and get an answer
        final_response = self.execute()
        
        # Save the final assistant answer into memory for future turns
        if final_response:
            self.messages.append({"role": "assistant", "content": final_response})
            
        # Return the final answer to the user
        return final_response

    # AGENT EXECUTOR LOOP: Connects the LLM's decisions with Python tool execution
    def execute(self, max_iterations: int = 5) -> str:
        # Limit the loop to prevent infinite tool-calling cycles
        for step in range(max_iterations):
            # Send full chat history and available tool schemas to the LLM
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto"  # Let the LLM decide whether to call a tool or reply directly
            )

            # Extract the LLM's response message
            response_message = completion.choices[0].message

            # Check if the LLM requested to run one or more tools
            if response_message.tool_calls:
                # Save the LLM's tool-call request in memory (required by the API format)
                self.messages.append(response_message)

                # Loop through every tool the LLM wants to execute
                for tool_call in response_message.tool_calls:
                    # Get the function name and parse JSON arguments into a Python dict
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)

                    print(f"  ⚙️ [Executor] Calling {fn_name}({fn_args})...")

                    # Look up the function in our registry and execute it safely
                    if fn_name in self.registry:
                        try:
                            result = self.registry[fn_name](**fn_args)
                        except Exception as e:
                            # Pass any runtime error back so the LLM can understand what went wrong
                            result = f"Tool Error: {str(e)}"
                    else:
                        result = f"Error: Tool '{fn_name}' not registered."

                    # Append the tool's output (observation) to memory with its matching ID
                    self.messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": fn_name,
                        "content": str(result)
                    })
                
                # Restart the loop so the LLM can read the tool output and form a final answer
                continue

            # If no tools were called, return the LLM's direct natural language answer
            return response_message.content

        # Fallback message if the agent hits the maximum step limit
        return "Sorry, I took too many steps to process your request."