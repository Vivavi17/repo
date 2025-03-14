import random
import time

import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.count_request = 5
        self.time_limiter_sec = 3
        self.key = "rate"

    def test(self) -> bool:
        self.redis_client.set(
            self.key, self.count_request, ex=self.time_limiter_sec, nx=True
        )
        current_count = self.redis_client.get(self.key)
        if int(current_count) == 0:
            return False
        self.redis_client.decrby(self.key, 1)
        return True


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == "__main__":
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    rate_limiter = RateLimiter(redis_client)

    for _ in range(50):
        time.sleep(random.randint(1, 2))
        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
