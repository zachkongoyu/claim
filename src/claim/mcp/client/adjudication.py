from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


class AdjudicationClient:
    def __init__(self, command: list[str], env: dict[str, str] | None = None) -> None:
        self._command = command
        self._env = env
        self._exit_stack: AsyncExitStack | None = None
        self._session: ClientSession | None = None

    async def __aenter__(self) -> "AdjudicationClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def connect(self) -> None:
        if self._session is not None:
            return
        self._exit_stack = AsyncExitStack()
        params = StdioServerParameters(command=self._command, env=self._env)
        read, write = await self._exit_stack.enter_async_context(stdio_client(params))
        self._session = await self._exit_stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()

    async def close(self) -> None:
        if self._exit_stack is None:
            return
        await self._exit_stack.aclose()
        self._exit_stack = None
        self._session = None

    async def _call_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        if self._session is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        result = await self._session.call_tool(name, args)
        if hasattr(result, "model_dump"):
            return result.model_dump()
        return {"result": result}

    async def validate_claim(self, claim: dict[str, Any]) -> dict[str, Any]:
        return await self._call_tool("validate_claim", {"payload": claim})

    async def translate_code(self, code: str, system: str, value_set_url: str) -> dict[str, Any]:
        return await self._call_tool(
            "translate_code",
            {"code": code, "system": system, "value_set_url": value_set_url},
        )

    async def apply_rules(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._call_tool("apply_rules", {"payload": payload})

    async def generate_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._call_tool("generate_response", {"payload": payload})
