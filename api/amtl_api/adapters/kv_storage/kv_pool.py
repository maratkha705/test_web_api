# from dataclasses import dataclass
from json import dumps, loads
from datetime import datetime
from redis.asyncio import ConnectionPool, Redis


class RedisStorage:
    dsn: str
    pool: ConnectionPool | None = None

    async def connect(self):
        self.pool = ConnectionPool.from_url(self.dsn)

    async def set(self, key: str, value: str | int | float | dict | list, expire: int = 60 * 60 * 7) -> bool | None:
        async with Redis.from_pool(self.pool) as client:

            if isinstance(value, dict) or isinstance(value, list):
                value: str = dumps(value, default=str, ensure_ascii=False)
            else:
                value: bytes = value.encode()
            return await client.set(name=key, value=value, ex=expire)

    async def get(self, key: str, value_type: str = "str") -> str | dict | list | None:
        async with Redis.from_pool(self.pool) as client:
            data: bytes = await client.get(key)
            if data:
                data: str = data.decode()
                if data[0] in ("[", "{"):
                    data = loads(data)
                else:
                    match value_type: # noqa pycharm
                        case "int":
                            data: int = int(data)
                        case "float":
                            data: float = float(data)
                        case "datetime":
                            data: datetime = datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f")
                        case _:
                            ...
                return data
            return None

    async def delete(self, key: str) -> None:
        async with Redis.from_pool(self.pool) as client:
            await client.delete(key)
