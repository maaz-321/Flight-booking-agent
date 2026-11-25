import json
from groq import Groq


class FlightBookingAgent:
    def __init__(self, client: Groq, model: str, system: str, tools: list, registry: dict) -> None:
        self.client = client
        self.model = model
        self.messages: list = [{"role": "system", "content": system}]
        self.tools = tools
        self.registry = registry

    # REQUEST HANDLER
    def __call__(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})
        final_response = self.execute()
        if final_response:
            self.messages.append({"role": "assistant", "content": final_response})
        return final_response

    # AGENT EXECUTOR LOOP
    def execute(self, max_iterations: int = 5) -> str:
        for step in range(max_iterations):
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto"
            )

            response_message = completion.choices[0].message

            # Agar LLM ne tool call manga hai
            if response_message.tool_calls:
                self.messages.append(response_message)

                for tool_call in response_message.tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments)

                    print(f"  ⚙️ [Executor] Calling {fn_name}({fn_args})...")

                    if fn_name in self.registry:
                        try:
                            result = self.registry[fn_name](**fn_args)
                        except Exception as e:
                            result = f"Tool Error: {str(e)}"
                    else:
                        result = f"Error: Tool '{fn_name}' not registered."

                    self.messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": fn_name,
                        "content": str(result)
                    })
                continue

            # Final natural language jawab
            return response_message.content

        return "Sorry, I took too many steps to process your request."