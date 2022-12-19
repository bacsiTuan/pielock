#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from redis import StrictRedis

from pie_lock.backends.base_lock import BaseLock


class OptimisticLock(BaseLock):
    url_scheme = "optimistic_lock"

    def get_client(self, **connection_args) -> None:
        host = str(connection_args.get("host")) or "localhost"
        port = int(connection_args.get("port")) or 6379
        password = str(connection_args.get("password"))
        db = int(connection_args.get("db")) or 0
        username = str(connection_args.get("username")) or None
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

    def __init__(self, expires: int, timeout: int, tries=32, prefix="", retry_after=1):
        super(OptimisticLock, self).__init__(expires, timeout, tries, prefix, retry_after)
        self.start_time = time.time()

    def acquire(self, redis_key: str) -> [bool, str]:
        redis = self.client
        if not redis:
            return False, "No redis client found"
        key = self.prefix + redis_key
        allowed = redis.setnx(key, "ok")
        if not allowed:
            return False, "Lock already acquired by another process"
        redis.expire(key, int(self.expires))
        return True, "Lock acquired key: {}".format(key)

    def release(self, redis_key: str) -> [bool, str]:
        redis = self.client
        if not redis:
            return False, "No redis client found"
        key = self.prefix + redis_key
        redis.delete(key)
        return True, "Lock released key: {}".format(key)
