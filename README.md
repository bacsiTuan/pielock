# Pie-lock
All lock module  using redis for control.

Installation
``` bash
pip install pie-lock
```

Usage Distributed Lock
``` bash
key = "test1"
success, msg = redis_lock.acquire(key)
print(msg)
if not success:
    print(msg)
redis_lock.release(key)
```

Usage Optimistic Lock
``` bash
def test_optimistic_lock(self):
    is_locked1, msg = redis_lock.acquire("key1")
    if not is_locked1:
        print(msg)
    is_locked2, msg = redis_lock.acquire("key1")
    if not is_locked2:
        print(msg)
    is_locked3, msg = redis_lock.acquire("key1")
    if not is_locked3:
        print(msg)
    release, msg = redis_lock.release("key1")
    if not release:
        print(msg)
    is_locked4, msg = redis_lock.acquire("key1")
    if not is_locked4:
        print(msg)
```
Configuration
-------------

Redis configuration
``` bash
from pie_lock.backends import OptimisticLock

redis_lock = DistributedLock(
    expires=5,
    timeout=5,
    retry_after=1, # seconds between retries
    tries=32,  # max number of tries
)
redis_lock.get_client(
    host="localhost",
    port=19821,
    password="passsword",
    username="default"
)


Note: all fields after the scheme are optional, and will default to
localhost on port 6379, using database 0.


``DEFAULT_TIMEOUT`` (default: 60)
```

If another client has already obtained the lock, sleep for a maximum of
this many seconds before giving up. A value of 0 means no wait (give up
right away).

The default timeout can be overridden when instantiating the lock.

``DEFAULT_EXPIRES`` (default: 10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We consider any existing lock older than this many seconds to be invalid
in order to detect crashed clients. This value must be higher than it
takes the critical section to execute.

The default expires can be overridden when instantiating the lock.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
