from time import time
from typing import Optional

from g4f_test import main,g4f_no_prov

f'''
# protected
TODOS:
- Allow configuring the output format of the measured time.
- Provide a way to measure the memory usage of a function.
'''
class LogTime:
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.secs = f"{round(time() - self.start, 2)} secs"

    def log_time(self, method: callable, **kwargs) -> Optional[str]:
        start = time()
        result = method(**kwargs)
        secs = f"{round(time() - start, 2)} secs"
        if result:
            return " ".join([result, secs])
        return secs

    async def log_time_async(self, method: callable, **kwargs) -> Optional[str]:
        result = await method(**kwargs)
        if result:
            return " ".join([result, self.secs])
        return self.secs

    def log_time_yield(self, method: callable, **kwargs):
        start = time()
        result = yield from method(**kwargs)
        yield f" {round(time() - start, 2)} secs"


if __name__ == "__main__":
    with LogTime() as log_time:
        result_sync = log_time.log_time(g4f_no_prov)
        print(result_sync)

    '''
    # protected
    description:
        The LogTime class provides a way to measure the time taken by a function.
    # protected
    usage:
        - Create an instance of the LogTime class.
        - Use the log_time method to measure the time taken by a synchronous function.
        - Use the log_time_async method to measure the time taken by an asynchronous function.
        - Use the log_time_yield method with a generator function to measure the time taken by the generator function.
    # protected
    predicted use cases:
        - Measuring the time taken by a function to optimize its performance.
        - Debugging and profiling functions to identify bottlenecks.
    # protected
    proposed features:
        - Allow configuring the output format of the measured time.
        - Provide a way to measure the memory usage of a function.
    '''
