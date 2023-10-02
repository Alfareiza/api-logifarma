from fastapi import status
from fastapi.responses import JSONResponse



def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Hacen falta 1 o más campos."}
    )
