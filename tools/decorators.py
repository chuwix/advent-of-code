from functools import wraps


def to_list(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))

    return wrapper
