from fastapi import APIRouter

base_router = APIRouter()


@base_router.get('/', status_code=200)
def root():
    return {"status": "ok"}
