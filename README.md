# Pie-lock

<p align="center">
    <em>Lock modules using redis</em>
</p>
<a href="https://pypi.org/project/pie-lock" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/pie-lock" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>

## Installation
With Pypi:
``` bash
pip install pie-lock
```

With Github:
``` bash
pip install git+https://github.com/bacsiTuan/pielock.git
```

## Usage Distributed Lock
``` python
key = "test1"
success, msg = redis_lock.acquire(key)
print(msg)
if not success:
    print(msg)
redis_lock.release(key)
```

## Usage Optimistic Lock
``` python
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
## Configuration

Redis configuration
``` python
from pie_lock.backends import DistributedLock

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
```

Note: all fields after the scheme are optional, and will default to
localhost on port 6379, using database 0.


``DEFAULT_TIMEOUT`` (default: 60)

If another client has already obtained the lock, sleep for a maximum of
this many seconds before giving up. A value of 0 means no wait (give up
right away).

The default timeout can be overridden when instantiating the lock.

## Limiter
Based on sliding window algorithm
``` python
from pie_lock.backends import Limiter, TimeUnit

redis = Limiter(
    host="localhost",
    port=19821,
    password="passsword",
    username="default",
    socket_timeout=2,
)

for i in range(6):
    allow, msg = redis.allow(redis_key="mylist", per=TimeUnit.SECOND, count=2)
    if not allow:
        print(msg)
time.sleep(1)
allow, msg = redis.allow(redis_key="mylist", per=TimeUnit.SECOND, count=2)
if not allow:
    print(msg)
```

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We consider any existing lock older than this many seconds to be invalid
in order to detect crashed clients. This value must be higher than it
takes the critical section to execute.

The default expires can be overridden when instantiating the lock.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
