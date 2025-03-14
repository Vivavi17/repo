import json

import redis


class RedisQueue:
    def __init__(self, redis_client: redis.Redis, queue_name: str):
        self.redis_client = redis_client
        self.queue_name = queue_name

    def publish(self, message: dict):
        redis_client.rpush(self.queue_name, json.dumps(message).encode("utf-8"))

    def consume(self) -> dict:
        message = self.redis_client.lpop(self.queue_name)
        if message:
            return json.loads(message)


if __name__ == "__main__":
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    q = RedisQueue(redis_client, "default")
    q.publish({"a": 1})
    q.publish({"b": 2})
    q.publish({"c": 3})

    assert q.consume() == {"a": 1}
    assert q.consume() == {"b": 2}
    assert q.consume() == {"c": 3}
