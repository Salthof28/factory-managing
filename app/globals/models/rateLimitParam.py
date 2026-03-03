from typing import TypedDict

class RateLimitParam(TypedDict):
    countReq: int
    maxReq: int
    timeRequest: float 
    maxTimeRequest: float