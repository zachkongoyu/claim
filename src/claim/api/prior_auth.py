from typing import Any

import sys

from fastapi import APIRouter

from agents.prior_auth_agent import PriorAuthAgent
from mcp.client.prior_auth import PriorAuthClient


router = APIRouter(prefix="/prior-auth", tags=["prior-auth"])


def _client() -> PriorAuthClient:
    return PriorAuthClient(
        transport="stdio",
        command=[sys.executable, "-m", "claim.mcp.server.prior_auth"],
    )


@router.post("/run")
async def run_prior_auth(payload: dict[str, Any]) -> dict[str, Any]:
    async with _client() as client:
        agent = PriorAuthAgent(client=client)
        return await agent.run(payload)
