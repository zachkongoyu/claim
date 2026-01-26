from __future__ import annotations

from typing import Any

from mcp.client.prior_auth import PriorAuthClient


class PriorAuthAgent:
    """Thin agent wrapper for prior-auth MCP tools."""

    def __init__(self, *, client: PriorAuthClient) -> None:
        self._client = client

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def predict_required(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.predict_required(payload)

    async def fetch_rules(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.fetch_rules(payload)

    async def build_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.build_request(payload)

    async def track_status(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.track_status(payload)
