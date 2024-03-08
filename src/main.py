from fastapi import FastAPI
from src.auth.router import router
from src.database import init, shutdown
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init()

@app.on_event("shutdown")
async def shutdown_event():
    await shutdown()

app = FastAPI(
    title="Fishka",
    version="0.1.0",
    contact={"whoami": "Ryzhik", "tg": "@printmyname"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8888"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

register_tortoise(
    app,
    db_url="sqlite://fshk.db",
    modules={"models": ["src.auth.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)