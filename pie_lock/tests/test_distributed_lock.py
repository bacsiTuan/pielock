#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
from pie_lock.backends import DistributedLock
import unittest

redis_lock = DistributedLock(
    expires=5,
    timeout=5,
    retry_after=1,
    tries=32,
)
redis_lock.get_client(
    host="localhost",
    port=19821,
    password="password",
    username="default",
    db=0
)


def test_lock():
    t1 = threading.Thread(target=__lock2, daemon=True)
    t2 = threading.Thread(target=__lock3, daemon=True)
    t3 = threading.Thread(target=__lock1, daemon=True)

    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()


def __lock2():
    time.sleep(0.5)
    try:
        redis_lock.acquire("test-redsync")
        print("locked2.1")
        redis_lock.release("test-redsync")
        print("done 2.2")
    except Exception as e:
        print(e)


def __lock3():
    try:
        redis_lock.acquire("test-redsync")
        print("locked3.1")
        time.sleep(2)
        redis_lock.release("test-redsync")
        print("done 3.2")
    except Exception as e:
        print(e)


def __lock1():
    time.sleep(0.9)
    try:
        redis_lock.acquire("test-redsync")
        print("locked1.1")
        time.sleep(2)
        redis_lock.release("test-redsync")
        print("done 1.2")
    except Exception as e:
        print(e)


class TestDistributedLock(unittest.TestCase):
    def test_distributed_lock(self):
        test_lock()

    def test_benchmark_distributed_lock100t(self):
        for i in range(100):
            key = "test{}".format(i)
            success, msg = redis_lock.acquire(key)
            print(msg)
            if not success:
                print(msg)
            redis_lock.release(key)

    def test_benchmark_distributed_lock1000t(self):
        for i in range(1000):
            key = "test{}".format(i)
            success, msg = redis_lock.acquire(key)
            print(msg)
            if not success:
                print(msg)
            redis_lock.release(key)
