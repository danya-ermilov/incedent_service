from fastapi import FastAPI
from app.api import routes
from app.db.session import engine
from app.models import Base


app = FastAPI(title="Incidents API")
app.include_router(routes.router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
