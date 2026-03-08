from google.adk.agents import Agent
from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()

class Data_Uploader_Agent:

    def __init__(self):
        self.agent=Agent(
            name="Data_Uploader_Agent",
            model="gemini-2.5-flash",
        )

    async def call__data_upload_mcp_tools(self):


        client = Client("http://localhost:9000/mcp")

        async with client:

            result = await client.call_tool(
                "call_Data_Upload_Engine"
            )

            return result