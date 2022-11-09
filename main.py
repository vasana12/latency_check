import math
from fastapi import FastAPI
from fastapi import Request
from datetime import datetime, timezone, timedelta
from log import logger
import random
app = FastAPI()

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = datetime.now().timestamp()*1000 - start_time.timestamp()*1000
    # unix_timestamp = (datetime.now(timezone.utc) + timedelta(days=3)).timestamp() * 1e3
    logger.debug(f"{int(start_time.timestamp()*1000)}\t{request.method}\t{request.url}\t{response.status_code}\t{process_time}")


@app.get("/pi")
def calculate_pi():
    pi = 0
    pi_mutipler = random.randint(0, 100000)

    for i in range(0, pi_mutipler):
        pi = math.pi
        pi = pi * 89897897
        pi += 1
    return {"success": True, "result": pi}
