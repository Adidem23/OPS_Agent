import time
import logging
from fastapi import APIRouter, HTTPException
from Controllers.client_class import Agent_Client_Class 
from Views.userQuery import userBackendQuery

logger = logging.getLogger("Main_server")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)


router = APIRouter(prefix="/OPS_BOT")


@router.get("/")
def breathingMessage():

    logger.info("Health check endpoint called")

    return {"message": "Server is Up and Running!!"}


@router.post("/process")
async def processUserQuery(query:userBackendQuery):

    user_query=query.userQuery

    SUPERVISOR_NODE_URL="http://localhost:8007"

    new_client=Agent_Client_Class()

    try:

        logger.info("Started talking to Supervisor ndoe")

        new_client=Agent_Client_Class()

        response= await new_client.create_connection(SUPERVISOR_NODE_URL,user_query)

        if(response):
            return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )

