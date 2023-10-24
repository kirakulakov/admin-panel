import asyncio
from typing import Coroutine, Any, Tuple


async def gather_with_exc_handling(*coros: Coroutine[Any, Any, Any]) -> Tuple[Any, ...]:
    results = await asyncio.gather(*coros, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            raise result

    return results
