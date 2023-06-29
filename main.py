from fastapi import FastAPI

from resources.routes import api_router

app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
async def startup():
    pass
    # await database.connect()


@app.on_event("shutdown")
async def startup():
    pass
    # await database.disconnect()
