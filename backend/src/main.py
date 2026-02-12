from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api import user_routers
from .configs import create_db_and_tables

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # startup
    from .models import UserPersistence
    create_db_and_tables()
    yield
    # shutdown (nếu cần)

app = FastAPI(lifespan=lifespan)

app.include_router(user_routers)

for route in app.routes:
    methods = ",".join(route.methods or [])
    print(f"{methods:15} {route.path:30} {route.name}")