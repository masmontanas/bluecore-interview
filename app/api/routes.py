from fastapi import APIRouter, Request, HTTPException, status
from app.services.redis import get_redis
import logging
from app.models.count import CountResponse, HealthCheckResponse

_logger = logging.getLogger(__name__)

_COUNTER_NAME = "counter"
_SERVICE_UNAVAILABLE_MESSAGE = "Service unavailable"


def get_router() -> APIRouter:
    router = APIRouter()

    @router.get("/healthz", response_model=HealthCheckResponse)
    async def healthcheck():
        return HealthCheckResponse

    @router.get("/", response_model=CountResponse)
    async def get_count(request: Request):
        try:
            redis = await get_redis(request)
            value = await redis.get(_COUNTER_NAME)
            count = int(value) if value else 0
            return CountResponse(count=count)
        except ConnectionError as e:
            _logger.error(str(e))
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=_SERVICE_UNAVAILABLE_MESSAGE)
        except Exception as e:
            _logger.error(str(e))
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=_SERVICE_UNAVAILABLE_MESSAGE)

    @router.post("/", response_model=CountResponse)
    async def increment_count(request: Request):
        try:
            redis = await get_redis(request)
            value = await redis.incr(_COUNTER_NAME)
            return CountResponse(count=value)
        except ConnectionError as e:
            _logger.error(str(e))
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=_SERVICE_UNAVAILABLE_MESSAGE)
        except Exception as e:
            _logger.error(str(e))
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=_SERVICE_UNAVAILABLE_MESSAGE)

    return router
