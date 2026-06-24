from fastapi import FastAPI

from app.api.routers.table_router import router

app = FastAPI()

app.include_router(router)