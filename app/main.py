# app/main.py
from fastapi import FastAPI
from .routers import logs, applications
from .database import engine, Base

app = FastAPI(title="Logs API")

app.include_router(logs.router)
app.include_router(applications.router)


@app.on_event("startup")
async def on_startup():
    # Создаем таблицы, если их нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
