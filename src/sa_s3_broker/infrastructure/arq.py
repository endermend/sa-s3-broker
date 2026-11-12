from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

_arq_pool: ArqRedis | None = None

async def init_arq(redis_settings: RedisSettings) -> ArqRedis:
    global _arq_pool
    if _arq_pool is None:
        _arq_pool = await create_pool(redis_settings)
    return _arq_pool

async def close_arq() -> None:
    global _arq_pool
    if _arq_pool:
        await _arq_pool.aclose()
        _arq_pool = None

def get_arq_pool() -> ArqRedis:
    if _arq_pool is None:
        raise RuntimeError("ARQ pool is not initialized")
    return _arq_pool