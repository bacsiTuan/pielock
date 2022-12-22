#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from redis import StrictRedis

from pie_lock.backends.base_lock import BaseLock


class DistributedLock(BaseLock):
    url_scheme = "distributed_lock"

    def get_client(self, **connection_args) -> None:
        host = connection_args.get('host') or 'localhost'
        port = connection_args.get('port') or 6379
        password = connection_args.get('password') or None
        db = connection_args.get('db') or 0
        username = connection_args.get('username') or None
        connection_pool = connection_args.get('connection_pool') or None
        self.client = StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password,
            username=username,
            connection_pool=connection_pool,
        )

    def __init__(self, expires: int, timeout: int, tries=32, prefix="", retry_after=1):
        super(DistributedLock, self).__init__(expires, timeout, tries, prefix, retry_after)
        self.start_time = time.time()

    def acquire(self, redis_key: str) -> [bool, str]:
        redis = self.client
        if not redis:
            return False, "No redis client found"
        timeout = self.timeout
        key = self.prefix + redis_key
        retry = 0
        while timeout >= 0 and retry <= self.tries:
            expires = time.time() + self.expires + 1

            if redis.setnx(key, expires):
                # We gained the lock; enter critical section
                self.start_time = time.time()
                redis.expire(key, int(self.expires))
                return True, "Lock acquired key: {}".format(key)

            current_value = redis.get(key)

            # If we found an expired lock by God knows how
            if current_value and float(current_value) < time.time():
                # Nobody raced us to replacing it
                if redis.getset(key, expires) == current_value:
                    self.start_time = time.time()
                    redis.expire(key, int(self.expires))
                    return True, "Lock acquired key: {}".format(key)

            timeout -= 1
            if timeout >= 0:
                retry += 1
                time.sleep(self.retry_after)
        return False, "Timeout while waiting for lock"

    def release(self, redis_key: str) -> [bool, str]:
        redis = self.client
        if not redis:
            return False, "No redis client found"
        key = self.prefix + redis_key
        # Only delete the key if we completed within the lock expiration,
        # otherwise, another lock might have been established
        # if time.time() - self.start_time < self.expires:
        redis.delete(key)
        return True, "Lock released key: {}".format(key)
