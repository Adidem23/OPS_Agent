import time
from fastapi import APIRouter
from create_data import OpsDataGenerator

router=APIRouter(prefix="/userquery")

@router.get("/")
def breathingMessage():
    return {"message":"Server is Up and Running!!"}

@router.post("/process")
async def processUserQuery():
    generator = OpsDataGenerator()

    try:

        start = time.time()

        generator.generate_batch()

        end = time.time()

        generator.logger.info(
            f"Batch completed in {round(end-start,2)} seconds"
        )

        return {"message": f"Batch completed in {round(end-start,2)} seconds"}

    except Exception as e:

        generator.logger.error(f"Generator error: {e}")
        
        return {"message": f"Generator error: {e}"}

    finally:

        generator.close()
