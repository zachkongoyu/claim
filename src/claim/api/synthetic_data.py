from typing import Any

import sys

from fastapi import APIRouter

from agents.synthetic_data_agent import SyntheticDataAgent
from mcp.client.synthetic_data import SyntheticDataClient


router = APIRouter(prefix="/synthetic-data", tags=["synthetic-data"])


def _client() -> SyntheticDataClient:
    return SyntheticDataClient(
        transport="stdio",
        command=[sys.executable, "-m", "claim.mcp.server.synthetic_data"],
    )


@router.post("/run")
async def run_synthetic_data(payload: dict[str, Any]) -> dict[str, Any]:
    async with _client() as client:
        agent = SyntheticDataAgent(client=client)
        return await agent.run(payload)
