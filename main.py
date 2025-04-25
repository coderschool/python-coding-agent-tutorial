import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import json

from utils.console import Console
from tools import ToolDefinition, read_file_tool, list_files_tool, edit_file_tool

load_dotenv()

api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    Console.error("DEEPSEEK_API_KEY not found in .env")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/")
MODEL = "deepseek-chat"

class Agent:
    def __init__(self, client_instance, tool_definitions: list[ToolDefinition] = []):
        self.client = client_instance
        self.tool_definitions = {tool.name: tool for tool in tool_definitions}  # Convert to dict for faster lookup

    def execute_tool_call(self, tool_call):
        try:
            tool_name = tool_call.function.name
            tool_args_str = tool_call.function.arguments
            
            if tool_name not in self.tool_definitions:
                return f"Error: Tool '{tool_name}' not found"
            tool_args = json.loads(tool_args_str)
            result = self.tool_definitions[tool_name].function(**tool_args)
            return result
        except Exception as e:
            return f"Error processing tool call: {str(e)}"

    def run_inference(self, conversation_history):
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=conversation_history,
                max_tokens=1024,
                tools=[tool.get_api_description() for tool in self.tool_definitions.values()],
            )
            return response.choices[0].message
        except Exception as e:
            Console.error(f"API Error: {e}")
            return None

    def run(self):
        conversation = []
        Console.info(f"Chatting with {MODEL}. Hit Ctrl+C to exit.")
        while True:
            try:
                user_input = Console.user("")
                if not user_input:
                    continue

                conversation.append({"role": "user", "content": user_input})
                
                while True:
                    assistant_message_obj = self.run_inference(conversation)
                    
                    if not assistant_message_obj:
                        if conversation and conversation[-1]["role"] == "user":
                            conversation.pop()
                        break
                    
                    assistant_message = assistant_message_obj.model_dump(exclude_unset=True)
                    conversation.append(assistant_message)
                    
                    if assistant_message_obj.content:
                        Console.assistant(MODEL, assistant_message_obj.content)
                    
                    if assistant_message_obj.tool_calls:
                        tool_call_responses = []
                        for tool_call in assistant_message_obj.tool_calls:
                            Console.tool_call(tool_call.function.name, tool_call.function.arguments)
                            tool_result = self.execute_tool_call(tool_call)                            
                            tool_response = {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_call.function.name,
                                "content": str(tool_result)
                            }
                            conversation.append(tool_response)
                            tool_call_responses.append(tool_response)
                        continue                    
                    break

            except KeyboardInterrupt:
                Console.info("\nExiting...")
                break
                
        Console.info("Agent run() finished.")


if __name__ == "__main__":
    agent_instance = Agent(client_instance=client, tool_definitions=[read_file_tool, list_files_tool, edit_file_tool])
    agent_instance.run()