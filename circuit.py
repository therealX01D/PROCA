from datetime import datetime
from .core import CircuitStatus

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitStatus.CLOSED

    def can_execute(self) -> bool:
        if self.state == CircuitStatus.CLOSED:
            return True
        elif self.state == CircuitStatus.OPEN:
            if (datetime.now().timestamp() - (self.last_failure_time or 0)) > self.timeout:
                self.state = CircuitStatus.HALF_OPEN
                return True
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitStatus.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now().timestamp()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitStatus.OPEN
