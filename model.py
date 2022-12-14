from typing import Optional, List
from datetime import datetime
from pytz import timezone
from pydantic import BaseModel

class PerformanceMonitorSchema(BaseModel):
    memory: int
    cpu: float
    check_time: int

class LatencyMonitorSchema(BaseModel):

    start_time_timestamp: int
    method: str
    url: str
    status_code: int
    latency: int


if __name__ == "__main__":
    print("main")

