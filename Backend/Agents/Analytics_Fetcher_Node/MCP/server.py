import httpx
import json
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("Analytics_Data_Engine_MCP")


@mcp.tool()
async def call_Analytics_Data_engine(scope_object):
    """
    Calls Analytics_Data_engine api 
    and forwards the package_name.
    """

    url = "http://localhost:8006/analytics_engine/process"

    try:
        async with httpx.AsyncClient(timeout=100) as client:
            response = await client.post(url,data=json.dumps(scope_object))

        return {
            "status_code": response.status_code,
            "response": response.json()
        }

    except Exception as e:
        return {
            "error": str(e)
        }


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

http_app=mcp.http_app(middleware=middleware)