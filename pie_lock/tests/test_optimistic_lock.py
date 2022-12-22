#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import queue
from pie_lock.backends import OptimisticLock
import unittest

redis_lock = OptimisticLock()
redis_lock.get_client(
    host="localhost",
    port=19821,
    password="boyhandsome",
    username="default",
    db=0,
    socket_timeout=2,
)

q = queue.Queue()


def worker():
    while True:
        item = q.get()
        is_locked1, msg = redis_lock.acquire(f"key{item}", 2)
        if not is_locked1:
            print(msg)
        is_release, msg = redis_lock.release(f"key{item}")
        if not is_release:
            print(msg)
        q.task_done()


# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for item in range(30):
    q.put(item)

# Block until all tasks are done.
q.join()


class TestOptimisticLock(unittest.TestCase):
    def test_optimistic_lock(self):
        is_locked1, msg = redis_lock.acquire("key1", 2)
        if not is_locked1:
            print(msg)
        is_locked2, msg = redis_lock.acquire("key1", 2)
        if not is_locked2:
            print(msg)
        is_locked3, msg = redis_lock.acquire("key1", 2)
        if not is_locked3:
            print(msg)
        release, msg = redis_lock.release("key1")
        if not release:
            print(msg)
        is_locked4, msg = redis_lock.acquire("key1", 2)
        if not is_locked4:
            print(msg)

    def test_benchmark_optimistic_100(self):
        for i in range(100):
            is_locked1, msg = redis_lock.acquire("key1", 2)
            if not is_locked1:
                print(msg)
            is_release, msg = redis_lock.release("key1")
            if not is_release:
                print(msg)

    def test_optimistic_lock_multi_thread(self):
        # Turn-on the worker thread.
        for i in range(25):
            threading.Thread(target=worker, daemon=True).start()

        # Send 10000 task requests to the worker.
        for item in range(10000):
            q.put(item)

        # Block until all tasks are done.
        q.join()




