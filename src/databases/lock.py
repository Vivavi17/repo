import datetime
import signal
import time
import unittest

import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def handler(signum, stack):
    raise TimeoutError


def single(max_processing_time: datetime.timedelta):
    signal.signal(signal.SIGALRM, handler)

    def decorator(func):
        f_name = func.__name__

        def wrapper(*args, **kwargs):
            while True:
                start = time.time()
                reserved = redis_client.set(
                    f_name, value=start, ex=max_processing_time.seconds, nx=True
                )

                if reserved:
                    signal.alarm(max_processing_time.seconds)
                    result = func(*args, **kwargs)
                    signal.alarm(0)
                    if redis_client.get(f_name) == start:
                        redis_client.delete(f_name)
                    return result

        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(seconds=2))
def process_transaction(i):
    time.sleep(i)


class TestFunc(unittest.TestCase):
    def test_large_func(self):
        with self.assertRaises(TimeoutError):
            process_transaction(3)


if __name__ == "__main__":
    unittest.main()
