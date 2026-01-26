from __future__ import annotations

from typing import Any

from mcp.client.synthetic_data import SyntheticDataClient


class SyntheticDataAgent:
    """Thin agent wrapper for synthetic-data MCP tools."""

    def __init__(self, *, client: SyntheticDataClient) -> None:
        self._client = client

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def generate_patient(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.generate_patient(payload)

    async def generate_claim(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.generate_claim(payload)

    async def generate_coverage(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.generate_coverage(payload)

    async def validate_resource(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.validate_resource(payload)

    async def export_dataset(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.export_dataset(payload)
