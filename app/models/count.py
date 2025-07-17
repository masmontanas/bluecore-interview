from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str = "ok"


class CountResponse(BaseModel):
    count: int

