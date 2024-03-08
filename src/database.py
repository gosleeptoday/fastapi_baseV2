from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url="sqlite://fshka.db",
        modules={"models": ["src.auth.models"]}
    )
    await Tortoise.generate_schemas()
async def shutdown():
    await Tortoise.close_connections()

