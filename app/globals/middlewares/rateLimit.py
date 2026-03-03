from fastapi import HTTPException, status
from ..models import RateLimitParam
from typing import Dict
from datetime import datetime, timezone

class RateLimit:
    def __init__(self):
        self.paramRate: Dict[str, RateLimitParam] = {}

    def used(self, ip: str):
        currentTime = datetime.now(timezone.utc)
        if ip not in self.paramRate:
            self.paramRate[ip] = {
                "countReq": 0,
                "maxReq": 10,
                "timeRequest": currentTime.timestamp(),
                "maxTimeRequest": 60
            }
            print(self.paramRate[ip]["timeRequest"])
        else:
            checkTimeReset = (currentTime).timestamp() - self.paramRate[ip]["timeRequest"]
            if checkTimeReset < self.paramRate[ip]["maxTimeRequest"]:
                self.paramRate[ip]["countReq"] += 1
                if self.paramRate[ip]["countReq"] > self.paramRate[ip]["maxReq"]:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Too Many Request")
            else:
                self.paramRate[ip] = {
                    "countReq": 0,
                    "maxReq": 10,
                    "timeRequest": currentTime.timestamp(),
                    "maxTimeRequest": 60
                }
              
        