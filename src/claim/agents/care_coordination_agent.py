from __future__ import annotations

from typing import Any

from mcp.client.care_coordination import CareCoordinationClient


class CareCoordinationAgent:
    """Thin agent wrapper for care-coordination MCP tools."""

    def __init__(self, *, client: CareCoordinationClient) -> None:
        self._client = client

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def aggregate_patient(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.aggregate_patient(payload)

    async def detect_gaps(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.detect_gaps(payload)

    async def suggest_interventions(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.suggest_interventions(payload)

    async def coverage_recommendations(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.coverage_recommendations(payload)
