from __future__ import annotations

from typing import Any

from mcp.client.fraud_detection import FraudDetectionClient


class FraudDetectionAgent:
    """Thin agent wrapper for fraud-detection MCP tools."""

    def __init__(self, *, client: FraudDetectionClient) -> None:
        self._client = client

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def analyze_bundle(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.analyze_bundle(payload)

    async def detect_anomalies(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.detect_anomalies(payload)

    async def generate_alerts(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.generate_alerts(payload)
