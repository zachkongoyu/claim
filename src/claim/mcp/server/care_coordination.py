from typing import Any

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("care-coordination-mcp")


@mcp.tool()
async def aggregate_patient(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "aggregate_patient", "payload": payload}


@mcp.tool()
async def detect_gaps(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "detect_gaps", "payload": payload}


@mcp.tool()
async def suggest_interventions(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "suggest_interventions", "payload": payload}


@mcp.tool()
async def coverage_recommendations(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "coverage_recommendations", "payload": payload}


if __name__ == "__main__":
    mcp.run()
