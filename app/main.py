from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, TypedDict
from app.users import users_router
from app.warehouse.routes import warehouse_router
from .globals.middlewares import RateLimit
from .globals.models import RateLimitParam
from datetime import datetime, timezone
# import time
# from app.warehouse.routes import WarehouseController

app = FastAPI()
# warehouseController = WarehouseController()

# example middleware for check time get response when hit path
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
    
requestData: Dict[str, RateLimitParam] = {}
rateLimit = RateLimit()
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    
    ip = str(request.client.host)
    try:
        rateLimit.used(ip)
    except HTTPException as exception:
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": exception.detail}
        )
    response = await call_next(request)
    return response
    
app.include_router(warehouse_router, prefix="/warehouse", tags=["Warehouse"])
app.include_router(users_router, prefix="/users", tags=["Users"])