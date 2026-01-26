from typing import Any

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("prior-auth-mcp")


@mcp.tool()
async def predict_required(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "predict_required", "payload": payload}


@mcp.tool()
async def fetch_rules(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "fetch_rules", "payload": payload}


@mcp.tool()
async def build_request(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "build_request", "payload": payload}


@mcp.tool()
async def track_status(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "track_status", "payload": payload}


if __name__ == "__main__":
    mcp.run()
