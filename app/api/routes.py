from fastapi import APIRouter

from app.api.endpoints import inventario

api_router = APIRouter()
# Routes {{baseUrl}}/v1/{{route}}
api_router.include_router(inventario.router, prefix="/inventario")
