from typing import Any

import sys

from fastapi import APIRouter

from agents.coding_translator_agent import CodingTranslatorAgent
from mcp.client.coding_translator import CodingTranslatorClient


router = APIRouter(prefix="/coding-translator", tags=["coding-translator"])


def _client() -> CodingTranslatorClient:
    return CodingTranslatorClient(
        transport="stdio",
        command=[sys.executable, "-m", "claim.mcp.server.coding_translator"],
    )


@router.post("/run")
async def run_coding_translator(payload: dict[str, Any]) -> dict[str, Any]:
    async with _client() as client:
        agent = CodingTranslatorAgent(client=client)
        return await agent.run(payload)
