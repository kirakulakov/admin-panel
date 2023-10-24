import asyncio


async def gather_with_exception_handling(*coros):
    results = await asyncio.gather(*coros, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            raise result
    return results
