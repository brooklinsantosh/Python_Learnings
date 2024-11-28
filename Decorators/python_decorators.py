import logging
from math import sqrt
from time import perf_counter
from typing import Callable, Any
import functools

logger = logging.getLogger('my_app')

def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for element in range(2, int(sqrt(number))+1):
        if number % element == 0:
            return False
    return True

def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(f"Execution of {func.__name__} took {run_time:.2f} seconds.")
        return value
    return wrapper

# def with_logging(logger: logging.Logger) -> Callable[..., Any]:
#     def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
#         @functools.wraps(func)
#         def wrapper(*args: Any, **kwargs: Any) -> Any:
#             logger.info(f"Calling {func.__name__}...")
#             value = func(*args, **kwargs)
#             logger.info(f"Finished calling {func.__name__}.")
#             return value
#         return wrapper
#     return decorator


def with_logging(func: Callable[..., Any],logger: logging.Logger) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Calling {func.__name__}...")
        value = func(*args, **kwargs)
        logger.info(f"Finished calling {func.__name__}.")
        return value
    return wrapper


with_default_logging = functools.partial(with_logging, logger=logger)

@with_default_logging
@benchmark
def count_prime_numbers(upper_bound: int) -> int:
    count = 0
    for number in range(upper_bound):
        if is_prime(number):
            count+=1
    return count

def main() -> None:
    logging.basicConfig(level= logging.INFO)
    # wrapper = benchmark(count_prime_numbers)
    # value = wrapper(100000)

    value = count_prime_numbers(100000)
    logging.info(f"Found {value} prime numbers.")

if __name__ == "__main__":
    main()
    