from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from exceptions import register_error_handlers
from shared.database import db_pool
from routers.user_account import router as user_account_router
from routers.monitored_url import router as monitored_url_router


@asynccontextmanager
async def app_lifecycle(app: FastAPI):
    await db_pool.db_connection_pool.open()
    yield
    await db_pool.db_connection_pool.close()

app = FastAPI(title='url-monitoring', lifespan=app_lifecycle)

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['GET', 'POST', 'DELETE', 'PATCH'],
                   allow_credentials=True,
                   allow_headers=['*']
                   )


@app.get("/", tags=["root"])
async def get_root():
    return JSONResponse(status_code=200, content="It's Alive!")

app.include_router(user_account_router)
app.include_router(monitored_url_router)
register_error_handlers(app)
