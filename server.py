from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

@mcp.tool()
async def get_icd10(diagnosis: str) -> [str]:
    '''Fetch ICD-10 codes for a given diagnosis from the CMS resources.
    Args:
        diagnosis: string representing the diagnosis to look up. e.g., "diabetes"
    '''
    url = f"https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search?sf=code,name&terms={diagnosis}&maxList=25"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    if not data or "results" not in data:
        return "No results found."

    alerts = []
    for item in data["results"]:
        code = item.get("code", "Unknown")
        name = item.get("name", "Unknown")
        alerts.append(f"{code}: {name}")

    return "\n---\n".join(alerts)
