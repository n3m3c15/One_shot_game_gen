import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
import pytz

load_dotenv()


class BaseAgent:
    def __init__(self,system_prompt,tools = None, **kwds):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version = '2024-12-01-preview',
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )

        self.deployment = 'gpt-4.1'

        self.tools_schema = tools or []
        self.tool_registry = {}
        skills = kwds.get('skills')
        self.system_prompt = system_prompt
        if skills:
            self.system_prompt += f'known skills:\n{skills}'
        
        self.messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        


    def register_tool(self, name: str, func):
        self.tool_registry[name] = func

    # Main agent loop
    def run(self, user_prompt: str):

        messages = self.messages
        messages.append({'role': 'user', "content": user_prompt})
        
        if self.tools_schema:
            response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            tools=self.tools_schema,
            tool_choice="auto"
        )
        else:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
            )

        message = response.choices[0].message

        # If tool call
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments or "{}")

            # Execute
            tool_result = self.execute_tool(tool_name, arguments)

            # Add tool result back into conversation
            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result)
            })

            # Second model call to generate final response
            final_response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages
            )

            return final_response.choices[0].message.content

        # If no tool used
        return message.content
    
    def execute_tool(self, tool_name, arguments):
        if tool_name not in self.tool_registry:
            raise ValueError(f"Tool {tool_name} not registered")

        return self.tool_registry[tool_name](**arguments)
