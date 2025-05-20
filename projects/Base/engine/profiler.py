import functools
import time
import sys

PROFILER = {}

TIME = time.time()


def profile():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()

            second = int(time.time() - TIME) + 1

            caller = sys._getframe(1)

            if func.__name__ not in PROFILER:
                PROFILER[func.__name__] = {
                    "name": func.__name__,
                    "display": caller.f_code.co_name,
                    "calls": {

                    }
                }

            if str(second) not in PROFILER[func.__name__]["calls"]:
                PROFILER[func.__name__]["calls"][str(second)] = []

            PROFILER[func.__name__]["calls"][str(second)].append(f"{end - start:.6f}")

            return result

        return wrapper

    return decorator


@profile()
def a(a):
    x = 0

    for i in range(int(a)):
        x += 1

    return x


# print(a(1e7))
# print(a(3e7))
# print(a(1e6))
# print(PROFILER)
