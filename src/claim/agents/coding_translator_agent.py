from __future__ import annotations

from typing import Any

from mcp.client.coding_translator import CodingTranslatorClient


class CodingTranslatorAgent:
    """Thin agent wrapper for coding-translator MCP tools."""

    def __init__(self, *, client: CodingTranslatorClient) -> None:
        self._client = client

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def map_codes(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.map_codes(payload)

    async def rank_candidates(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.rank_candidates(payload)

    async def validate_code(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.validate_code(payload)

    async def flag_ambiguity(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.flag_ambiguity(payload)
