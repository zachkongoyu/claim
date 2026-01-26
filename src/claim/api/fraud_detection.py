from typing import Any

import sys

from fastapi import APIRouter

from agents.fraud_detection_agent import FraudDetectionAgent
from mcp.client.fraud_detection import FraudDetectionClient


router = APIRouter(prefix="/fraud-detection", tags=["fraud-detection"])


def _client() -> FraudDetectionClient:
    return FraudDetectionClient(
        transport="stdio",
        command=[sys.executable, "-m", "claim.mcp.server.fraud_detection"],
    )


@router.post("/run")
async def run_fraud_detection(payload: dict[str, Any]) -> dict[str, Any]:
    async with _client() as client:
        agent = FraudDetectionAgent(client=client)
        return await agent.run(payload)
