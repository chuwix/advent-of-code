import time
from functools import wraps


def to_list(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))

    return wrapper


def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            res = f(*args, **kwargs)
            return res
        finally:
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"Finished in {elapsed_time:.3f}s")

    return wrapper


def print_result(*, start=None, end=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if start: print(start.format(*args))
            result = func(*args, **kwargs)
            if end:
                print(end.format(**kwargs))
            else:
                print(result)
            return result

        return wrapper

    return decorator
