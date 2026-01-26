from __future__ import annotations

from typing import Any, Awaitable, Callable, Iterable

from mcp.client.adjudication import AdjudicationClient


Planner = Callable[[dict[str, Any]], Awaitable[list[str]]]


class AdjudicationAgent:
    """Agent scaffold for adjudication MCP tools."""

    def __init__(
        self,
        *,
        client: AdjudicationClient,
        planner: Planner | None = None,
    ) -> None:
        self._client = client
        self._planner = planner

    async def validate_claim(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.validate_claim(payload)

    async def translate_code(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.translate_code(
            code=payload["code"],
            system=payload["system"],
            value_set_url=payload["value_set_url"],
        )

    async def apply_rules(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.apply_rules(payload)

    async def generate_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._client.generate_response(payload)

    async def run(self, claim: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError

    async def _select_plan(self, claim: dict[str, Any], context: dict[str, Any]) -> list[str]:
        raise NotImplementedError

    def _extract_code_targets(
        self,
        claim: dict[str, Any],
        context: dict[str, Any],
    ) -> Iterable[dict[str, str]]:
        raise NotImplementedError
