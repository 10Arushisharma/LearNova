import time
from collections import defaultdict, deque
from typing import Dict
from app.core.config import settings

try:
    import redis
except Exception:  # pragma: no cover
    redis = None


class RateLimiter:
    def __init__(self) -> None:
        self._memory_windows: Dict[str, deque[float]] = defaultdict(deque)
        self._redis_client = None
        try:
            if redis is not None and settings.REDIS_URL:
                client = redis.from_url(settings.REDIS_URL, socket_connect_timeout=0.4, socket_timeout=0.4)
                client.ping()
                self._redis_client = client
        except Exception:
            self._redis_client = None

    def allow(self, key: str, limit_per_minute: int) -> bool:
        now = time.time()
        window_start = now - 60.0

        if self._redis_client is not None:
            try:
                pipe = self._redis_client.pipeline()
                rkey = f"rl:{key}"
                pipe.zremrangebyscore(rkey, 0, window_start)
                pipe.zcard(rkey)
                pipe.zadd(rkey, {f"{now}": now})
                pipe.expire(rkey, 65)
                _, current_count, _, _ = pipe.execute()
                return int(current_count) < limit_per_minute
            except Exception:
                pass

        dq = self._memory_windows[key]
        while dq and dq[0] < window_start:
            dq.popleft()
        if len(dq) >= limit_per_minute:
            return False
        dq.append(now)
        return True


rate_limiter = RateLimiter()
