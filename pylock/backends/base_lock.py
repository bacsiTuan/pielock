#!/usr/bin/env python
# -*- coding: utf-8 -*-
class LockTimeout(BaseException):
    """Raised in the event a timeout occurs while waiting for a lock"""


class BaseLock(object):
    def __init__(self, expires: int, timeout: int, tries=32, prefix="", retry_after=1):
        """
        :param  client:  The the backend client instance to use.

        """
        self.expires = expires
        self.timeout = timeout
        self.client = None
        self.prefix = prefix
        self.tries = tries
        self.retry_after = retry_after

    @classmethod
    def get_client(cls, **connection_args):
        raise NotImplementedError

    def acquire(self, redis_key: str) -> [bool, str]:
        raise NotImplementedError

    def release(self, redis_key: str) -> [bool, str]:
        raise NotImplementedError
