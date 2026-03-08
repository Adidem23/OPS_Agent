import httpx
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("data_upload_mcp")


@mcp.tool()
async def call_Data_Upload_Engine():
    """
    Calls data_upload_engine api 
    and forwards the package_name.
    """

    url = "http://localhost:8005/data_upload_engine/process"

   
    try:
        async with httpx.AsyncClient(timeout=100) as client:
            response = await client.post(url)

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