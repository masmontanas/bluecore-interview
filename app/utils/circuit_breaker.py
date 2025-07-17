import logging
import time
from functools import wraps

_logger = logging.getLogger(__name__)


class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time=30):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.last_failure_time = 0
        self.open = False

    def is_open(self):
        if self.open:
            if (time.time() - self.last_failure_time) > self.recovery_time:
                self.reset()
            else:
                _logger.warning("Circuit breaker is OPEN, rejecting call")
        return self.open

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.open = True
            _logger.warning("Circuit breaker opened due to repeated Redis failures")

    def reset(self):
        self.failures = 0
        self.open = False
        _logger.info("Circuit breaker reset")

    def wrap(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.is_open():
                raise ConnectionError("Redis temporarily unavailable due to circuit breaker")
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                self.record_failure()
                raise e
        return wrapper
