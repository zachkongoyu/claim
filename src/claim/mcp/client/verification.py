import json
import os
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Optional

import anyio
import httpx

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


class VerificationMCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.http_client: Optional[httpx.AsyncClient] = None
        self.api_key = os.getenv("OPENROUTER_API_KEY") or "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"
        self.model = os.getenv("OPENROUTER_MODEL", "x-ai/grok-code-fast-1")
    # methods will go here

    async def _call_openrouter(self, messages, tools):
        """Call the OpenRouter chat endpoint with OpenAI-compatible payload."""
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")

        if self.http_client is None:
            self.http_client = await self.exit_stack.enter_async_context(
                httpx.AsyncClient(timeout=httpx.Timeout(60.0))
            )

        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "reasoning": {"enabled": True},
        }
        
        print("---------------------Payload-------------------")
        print("Calling OpenRouter with payload:", payload)
        print("---------------------Payload-------------------")

        response = await self.http_client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()

        print("---------------------Response-------------------")
        print("OpenRouter response:", response.json())
        print("---------------------Response-------------------")

        return response.json()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        is_module = not (is_python or is_js)

        if is_module:
            command = "python"
            args = ["-m", server_script_path]
        else:
            command = "python" if is_python else "node"
            args = [server_script_path]

        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using OpenRouter and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        } for tool in response.tools]

        final_text = []

        # Loop until the model stops requesting tool calls
        while True:
            completion = await self._call_openrouter(messages, available_tools)
            choice = completion["choices"][0]
            message = choice.get("message", {})

            content_text = message.get("content") or ""
            tool_calls = message.get("tool_calls", [])

            if tool_calls:
                # Append assistant message with tool calls so the model keeps context
                messages.append({
                    "role": "assistant",
                    "content": content_text,
                    "tool_calls": tool_calls,
                })

                # Execute each tool and feed results back
                for tool_call in tool_calls:
                    name = tool_call["function"]["name"]
                    raw_args = tool_call["function"].get("arguments", "{}")
                    parsed_args = json.loads(raw_args) if raw_args else {}

                    result = await self.session.call_tool(name, parsed_args)

                    print("--------------------Tool Call-------------------")
                    print(f"Tool: {name}")
                    print(f"Arguments: {parsed_args}")
                    print(f"Result: {result.content}")
                    print("--------------------Tool Call-------------------")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result.content[0].text,
                    })

                # Continue the loop to let the model observe tool outputs
                continue

            # No more tool calls; collect final text and exit
            final_text.append(content_text)
            break

        return "\n".join([text for text in final_text if text])

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

if __name__ == "__main__":
    async def main():
        client = VerificationMCPClient()
        try:
            await client.connect_to_server("claim.mcp.server.verification")
            await client.chat_loop()
        finally:
            await client.cleanup()

    anyio.run(main)