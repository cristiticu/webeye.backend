from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from shared.db_pool import db_connection_pool


@asynccontextmanager
async def app_lifecycle(app: FastAPI):
    await db_connection_pool.open()
    yield
    await db_connection_pool.close()

app = FastAPI(title='bully-tracker', lifespan=app_lifecycle)

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['GET', 'POST', 'DELETE', 'PATCH'],
                   allow_credentials=True,
                   allow_headers=['*']
                   )


@app.get("/", tags=["root"])
async def get_root():
    return JSONResponse(status_code=200, content="It's Alive!")
