from fastapi import APIRouter

def create_silver_router(faker_service):
    router = APIRouter(prefix="/silver", tags=["silver"])

    @router.post("/start")
    async def start_faker():
        await faker_service.start_loop()
        return {"status": "Faker loop started"}

    @router.post("/stop")
    def stop_faker():
        faker_service.stop_loop()
        return {"status": "Faker loop stopped"}

    return router