from fastapi import FastAPI
from app.routers import ALL_ROUTERS
app = FastAPI()

for router in ALL_ROUTERS:
    app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
