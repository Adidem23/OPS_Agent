import asyncio
from client_class import Agent_Client_Class


async def call_tools():
    new_client=Agent_Client_Class()
    
    AGENT_NODE_URL="http://localhost:8009"

    response= await new_client.create_connection(AGENT_NODE_URL,"Why sales are down in West India")

    print(response)


if __name__=="__main__":
    asyncio.run(call_tools())