import time
from functools import wraps


def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = f(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Finished in {elapsed_time:.3f}s")
        return res

    return wrapper
