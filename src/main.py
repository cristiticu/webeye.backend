import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from exceptions import register_error_handlers
from routers.user_account import router as user_account_router
from routers.monitored_webpage import router as monitored_webpage_router
from routers.auth import router as authentication_router
from routers.scheduled_tasks import router as scheduled_tasks_router
from routers.monitoring_events import router as monitoring_events_router


app = FastAPI(title='webpage monitoring',
              version='0.1.0',
              debug=settings.ENVIRONMENT != 'production'
              )

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['GET', 'POST', 'DELETE', 'PATCH'],
                   allow_credentials=True,
                   allow_headers=['*']
                   )


@app.get("/", tags=["root"])
async def get_root():
    return JSONResponse(status_code=200, content="It's Alive!")

app.include_router(authentication_router)
app.include_router(user_account_router)
app.include_router(monitored_webpage_router)
app.include_router(scheduled_tasks_router)
app.include_router(monitoring_events_router)

register_error_handlers(app)
