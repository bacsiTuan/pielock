#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from redis import StrictRedis


class TimeUnit(object):
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 3600 * 24
    WEEK = DAY * 7
    MONTH = WEEK * 4


class Limiter:
    def __init__(self,
                 host="localhost",
                 port=6379,
                 db=0,
                 password=None,
                 socket_timeout=None,
                 username=None,
                 connection_pool=None,
                 prefix=""
                 ):
        self.client = StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password,
            username=username,
            connection_pool=connection_pool,
            socket_timeout=socket_timeout,
        )
        self.prefix = prefix

    def allow(self, redis_key: str, per: int, count: int) -> [bool, str]:
        redis = self.client
        if not redis:
            return False, "No redis client found"
        key = self.prefix + redis_key
        current_time = int(time.time())
        print(redis.exists(key))
        if redis.exists(key) == 0:
            push = redis.rpush(key, current_time)
            print(push)
            redis.expire(key, per)
            return True, "First time"
        list_values = redis.lrange(key, 0, -1)
        print(list_values)
        if len(list_values) == 0:
            redis.rpush(key, current_time)
            redis.expire(key, per)
            return True, "First time"
        first_request_at = int((list_values[0]).decode("utf-8"))
        print(first_request_at)
        if len(list_values) == count and current_time - first_request_at <= per:
            return False, "Rate limit exceeded"
        if len(list_values) == count and current_time - first_request_at > per:
            pop = redis.lpop(key)
            print(f"pop old value {pop}")
            push = redis.rpush(key, current_time)
            print(f"push new value: {push}")
        if len(list_values) < count:
            push = redis.rpush(key, current_time)
            print(f"push new value: {push}")
        redis.expire(key, per)
        return True, f"Rate limit reached {count} requests per {per} seconds"
