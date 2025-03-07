import unittest.mock
from collections import deque


def lru_cache(func=None, *, maxsize=None):
    params_cache = deque(maxlen=maxsize)
    result_cache = deque(maxlen=maxsize)

    def decorator(func):
        def wrapper(*args, **kwargs):
            params = (args, kwargs)
            if params in params_cache:
                ind = params_cache.index(params)
                result = result_cache[ind]

                params_cache.remove(params)
                result_cache.remove(result)
            else:
                result = func(*args, **kwargs)

            params_cache.append(params)
            result_cache.append(result)
            return result

        return wrapper

    return decorator(func) if func else decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
