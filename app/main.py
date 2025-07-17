import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import get_router
from app.services.redis import close_redis_connection
from app.settings import get_settings
from app.lib.circuit_breaker import CircuitBreaker
from app.lib.logging import configure_json_logging


def create_app() -> FastAPI:
    """
    Use application factory to inject all dependencies.
    """
    settings = get_settings()
    configure_json_logging(settings.log_level)

    circuit_breaker = CircuitBreaker(
        failure_threshold=settings.redis_failure_threshold,
        recovery_time=settings.redis_recovery_time,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Manage startup/shutdown tasks related to the application lifecycle.
        """
        # Start serving requests
        yield
        await close_redis_connection(app)

    app = FastAPI(title="Async Counter API", lifespan=lifespan, version="0.0.1")
    app.state.settings = settings
    app.state.circuit_breaker = circuit_breaker
    app.include_router(get_router())

    return app


if __name__ == "__main__":
    """
    Start uvicorn to run the api locally for testing.
    """
    uvicorn.run("app.main:create_app", host="0.0.0.0", port=8000, factory=True)

else:
    app = create_app()
