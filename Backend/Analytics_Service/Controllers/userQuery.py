import time
import logging
from fastapi import APIRouter, HTTPException
# from Views.userQuery import InvestigationScope
from Analyze_data import InvestigationEngine
from fastapi import Request



logger = logging.getLogger("analytics_engine")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)


router = APIRouter(prefix="/analytics_engine")



@router.get("/")
def breathingMessage():

    logger.info("Health check endpoint called")

    return {"message": "Server is Up and Running!!"}


@router.post("/process")
async def processUserQuery(request:Request):

    start_time = time.time()

    try:

        body = await request.json()

        logger.info(f"Incoming investigation request | scope={body}")

        engine = InvestigationEngine()

        logger.info("Investigation engine initialized")

        report = engine.run(body)

        duration = round(time.time() - start_time, 3)

        logger.info(f"Investigation completed in {duration}s")

        return report

    except Exception as e:

        logger.exception("Investigation failed")

        raise HTTPException(
            status_code=500,
            detail="Analytics engine processing failed"
        )