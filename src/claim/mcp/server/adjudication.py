from typing import Any

from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("adjudication-mcp")


@mcp.tool()
async def validate_claim(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "validate_claim", "payload": payload}


@mcp.tool()
async def translate_code(code: str, system: str, value_set_url: str):
    """Validate a medical code using the HL7 Terminology Server."""
    base_url = "https://tx.fhir.org/r5"

    params = {
        "url": value_set_url,
        "code": code,
        "system": system,
    }

    async with AsyncClient() as client:
        response = await client.get(
            f"{base_url}/ValueSet/$validate-code",
            params=params,
            headers={"Accept": "application/fhir+json"},
        )

        response.raise_for_status()

        return response.json()


@mcp.tool()
async def apply_rules(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "apply_rules", "payload": payload}


@mcp.tool()
async def generate_response(payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "not_implemented", "tool": "generate_response", "payload": payload}


if __name__ == "__main__":
    mcp.run()