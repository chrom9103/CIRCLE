import re
from typing import Optional

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .routers import records as records_router
from .routers import auth as auth_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    print("RequestValidationError:", exc)
    return JSONResponse(status_code=422, content={"detail": exc.errors() if hasattr(exc, "errors") else str(exc)})


app.include_router(records_router.router)
app.include_router(auth_router.router)
