import logging
from redis.asyncio import Redis
from fastapi import Request
from app.utils.circuit_breaker import CircuitBreaker

_logger = logging.getLogger(__name__)


class RedisWithCircuitBreaker:
    """
    Wrap all Redis commands with the circuit breaker.
    """
    def __init__(self, redis: Redis, circuit_breaker: CircuitBreaker):
        self._redis = redis
        self._cb = circuit_breaker

    def __getattr__(self, name):
        orig_attr = getattr(self._redis, name)

        if callable(orig_attr):
            return self._cb.wrap(orig_attr)
        return orig_attr


async def get_redis(request: Request) -> RedisWithCircuitBreaker:
    circuit_breaker = getattr(request.app.state, "circuit_breaker", None)
    if circuit_breaker is None:
        raise RuntimeError("Circuit breaker is not configured")

    redis = getattr(request.app.state, "redis", None)
    if not redis:
        settings = request.app.state.settings
        try:
            redis_instance = Redis.from_url(
                settings.redis_url,
                decode_responses=True,
                max_connections=settings.redis_max_connections,
            )
            redis = RedisWithCircuitBreaker(redis_instance, circuit_breaker)
            request.app.state.redis = redis
        except Exception as e:
            _logger.error(f"Redis connection failed: {str(e)}")
            raise

    return redis


async def close_redis_connection(app):
    redis = getattr(app.state, "redis", None)
    if redis:
        try:
            redis_instance = getattr(redis, "_redis", redis)
            await redis_instance.close()
        except Exception as e:
            _logger.error(f"Error closing Redis connection: {str(e)}")
    app.state.redis = None
