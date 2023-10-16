from time import time
from typing import Optional


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

    def log_time_yield(self, method: callable, **kwargs) -> Optional[str]:
        start = time()
        result = yield from method(**kwargs)
        yield f" {round(time() - start, 2)} secs"


if __name__ == "__main__":
    with LogTime() as log_time:
        result_sync = log_time.log_time(main)
        print(result_sync)
