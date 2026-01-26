from typing import Any

import sys

from fastapi import APIRouter

from agents.care_coordination_agent import CareCoordinationAgent
from mcp.client.care_coordination import CareCoordinationClient


router = APIRouter(prefix="/care-coordination", tags=["care-coordination"])


def _client() -> CareCoordinationClient:
    return CareCoordinationClient(
        transport="stdio",
        command=[sys.executable, "-m", "claim.mcp.server.care_coordination"],
    )


@router.post("/run")
async def run_care_coordination(payload: dict[str, Any]) -> dict[str, Any]:
    async with _client() as client:
        agent = CareCoordinationAgent(client=client)
        return await agent.run(payload)
