#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from pie_lock.backends import Limiter, TimeUnit
import unittest
redis = Limiter(
    host="redis-19821.c295.ap-southeast-1-1.ec2.cloud.redislabs.com",
    port=19821,
    password="boyhandsome",
    username="default",
    db=0,
    socket_timeout=5,
)


class TestLimiter(unittest.TestCase):
    def test_limiter(self):
        allow, msg = redis.allow(redis_key="mylist", per=1*TimeUnit.MINUTE, count=2)
        print(allow)
        print(msg)

    def test_allow_sec(self):
        for i in range(6):
            allow, msg = redis.allow(redis_key="mylist", per=TimeUnit.SECOND, count=2)
            if not allow:
                print(msg)
        time.sleep(1)
        allow, msg = redis.allow(redis_key="mylist", per=TimeUnit.SECOND, count=2)
        if not allow:
            print(msg)

    def test_benchmark_allow_100t(self):
        for i in range(100):
            allow, msg = redis.allow(redis_key="mylist", per=TimeUnit.SECOND, count=5)
            if not allow:
                print(msg)

    def test_benchmark_allow_1000t(self):
        for i in range(1000):
            allow, msg = redis.allow(redis_key="mylist", per=TimeUnit.SECOND, count=5)
            if not allow:
                print(msg)

