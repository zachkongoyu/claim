from typing import Any

import sys

from fastapi import APIRouter

from agents.adjudication_agent import AdjudicationAgent
from mcp.client.adjudication import AdjudicationClient


router = APIRouter(prefix="/adjudication", tags=["adjudication"])


def _client() -> AdjudicationClient:
    return AdjudicationClient(
        transport="stdio",
        command=[sys.executable, "-m", "claim.mcp.server.adjudication"],
    )


@router.post("/run")
async def run_adjudication(payload: dict[str, Any]) -> dict[str, Any]:
    claim = payload.get("claim", payload)
    context = payload.get("context", {})
    async with _client() as client:
        agent = AdjudicationAgent(client=client)
        return await agent.run(claim, context)
