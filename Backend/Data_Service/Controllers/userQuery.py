import time
import logging
from fastapi import APIRouter, HTTPException
from create_data import OpsDataGenerator



logger = logging.getLogger("data_upload_engine")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)


router = APIRouter(prefix="/data_upload_engine")


@router.get("/")
def breathingMessage():

    logger.info("Health check endpoint called")

    return {"message": "Server is Up and Running!!"}



@router.post("/process")
async def processUserQuery():

    generator = OpsDataGenerator()

    start_time = time.time()

    try:

        logger.info("Starting synthetic data generation batch")

        generator.generate_batch()

        duration = round(time.time() - start_time, 3)

        logger.info(f"Batch completed successfully in {duration}s")

        return {
            "status": "success",
            "execution_time": duration
        }

    except Exception as e:

        logger.exception("Data generation batch failed")

        raise HTTPException(
            status_code=500,
            detail=f"Generator error: {str(e)}"
        )

    finally:

        try:
            generator.close()
            logger.info("Generator resources closed")
        except Exception:
            logger.warning("Generator close failed")