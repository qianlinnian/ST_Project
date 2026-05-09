from time import perf_counter


def measure_time(func, *args, **kwargs):
    start = perf_counter()
    result = func(*args, **kwargs)
    elapsed = perf_counter() - start
    return elapsed, result
