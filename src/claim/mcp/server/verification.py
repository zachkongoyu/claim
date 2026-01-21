import json

from fhir.resources import get_fhir_model_class
from fhir_core.fhirabstractmodel import FHIRAbstractModel
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Verification MCP Server")

@mcp.tool()
def validate_fhir(resource: str) -> bool:
    """
    Validates if the provided JSON is a valid 2026 FHIR R4/R5 resource.
    """

    try:
        data = json.loads(resource)
    except json.JSONDecodeError:
        return False

    resource_type = data.get("resourceType")
    if not resource_type:
        return False

    try:
        fhir_model_class: type[FHIRAbstractModel] = get_fhir_model_class(resource_type)
        fhir_model_class(**data)
        return True
    except Exception:
        return False

mcp.run(transport="stdio")
