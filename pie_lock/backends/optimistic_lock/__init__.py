#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from redis import StrictRedis


class OptimisticLock:
    url_scheme = "optimistic_lock"

    def get_client(self, **connection_args) -> None:
        host = connection_args.get("host") or "localhost"
        port = connection_args.get("port") or 6379
        password = connection_args.get("password") or None
        db = connection_args.get("db") or 0
        username = connection_args.get("username") or None
        connection_pool = connection_args.get("connection_pool") or None
        socket_timeout = connection_args.get("socket_timeout") or None
        self.client = StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password,
            username=username,
            connection_pool=connection_pool,
            socket_timeout=socket_timeout,
        )

    def __init__(self, prefix=""):
        self.client = None
        self.prefix = prefix
        self.start_time = time.time()

    def acquire(self, redis_key: str, expires: int) -> [bool, str]:
        redis = self.client
        if not redis:
            return False, "No redis client found"
        key = self.prefix + redis_key
        allowed = redis.setnx(key, "ok")
        if not allowed:
            return False, "Lock already acquired by another process"
        redis.expire(key, int(expires))
        return True, "Lock acquired key: {}".format(key)

    def release(self, redis_key: str) -> [bool, str]:
        redis = self.client
        if not redis:
            return False, "No redis client found"
        key = self.prefix + redis_key
        redis.delete(key)
        return True, "Lock released key: {}".format(key)
