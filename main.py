import math
from fastapi import FastAPI
from fastapi import Request
from datetime import datetime, timezone, timedelta
from log import logger

app = FastAPI()

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    start_time = (datetime.now(timezone.utc) + timedelta(days=3)).timestamp() * 1e3
    response = await call_next(request)
    process_time = (datetime.now(timezone.utc) + timedelta(days=3)).timestamp() * 1e3 - start_time
    logger.debug(f"{process_time}\t{request.url}\t{request.method}\t{response.status_code}")
    return response


@app.get("/pi")
def calculate_pi():
    pi = math.pi
    return {"success": True, "result": pi}
