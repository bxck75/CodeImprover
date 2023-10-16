from time import time
from typing import Any, Callable, Generator
f'''
# TODO: make the script log to a text log file
'''

class TimeLogger:
    def __init__(self, method: Callable[..., Any]):
        self.method = method

    async def __call__(self, **kwargs: Any) -> str:
        start = time()
        result = await self.method(**kwargs)
        secs = f"{round(time() - start, 2)} secs"
        if result:
            return " ".join([result, secs])
        return secs

    def __iter__(self) -> Generator[str, Any, None]:
        start = time()
        result = yield from self.method()
        yield f"{round(time() - start, 2)} secs"
        if result:
            yield result

    def __call__(self, **kwargs: Any) -> str:
        start = time()
        result = self.method(**kwargs)
        secs = f"{round(time() - start, 2)} secs"
        if result:
            return " ".join([result, secs])
        return secs


async def async_method(**kwargs: Any) -> str:
    # TODO: implement async_method
    return "async_method completed"


def generator_method() -> Generator[str, Any, None]:
    # TODO: implement generator_method
    yield "generator_method completed"


def sync_method(**kwargs: Any) -> str:
    # TODO: implement sync_method
    return "sync_method completed"


if __name__ == "__main__":
    async_logger = TimeLogger(async_method)
    print(async_logger.__name__)
    print(async_logger.__doc__)
    print(async_logger.__module__)

    async_result = async_logger(a=1, b=2)
    print(async_result)

    generator_logger = TimeLogger(generator_method)
    print(list(generator_logger()))

    sync_logger = TimeLogger(sync_method)
    sync_result = sync_logger(a=1, b=2)
    print(sync_result)


"""
Description:
    The TimeLogger class can be used to log the time taken by a method to execute. 
    It can be used with synchronous, asynchronous and generator functions. 

Usage:
    1. Instantiate a TimeLogger object with a method as argument.
    2. Call the object with the keyword arguments for the method.
    3. The logged time and return value (if any) are returned as a string.
    4. To use with a generator function, iterate over the TimeLogger object.
    5. To use with an asynchronous function, await the TimeLogger object.

Predicted use cases:
    1. Logging time taken by a function to execute.
    2. Benchmarking different implementations of a function.
    3. Measuring performance of code changes.

Proposed features:
    1. Add support for logging to a file.
    2. Add support for logging to a database.
    3. Add support for logging to a cloud service.
"""
