import asyncio
from fastmcp import Client


async def call_mcp_tools():

    client=Client(
        "http://localhost:9000/mcp"
    )

    async with client:
        result = await client.call_tool("call_Data_Upload_Engine")
        print(result)


if __name__=="__main__":
    asyncio.run(call_mcp_tools())