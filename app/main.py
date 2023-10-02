from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.endpoints.base import base_router
from app.api.routes import api_router
from app.exceptions import validation_exception_handler
from app.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, docs_url=None)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(base_router)
app.include_router(api_router, prefix='/v1')
