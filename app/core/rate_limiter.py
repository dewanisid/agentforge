from fastapi import HTTPException, Request, status
from app.db.redis import redis_client

async def rate_limit(request: Request, max_requests: int=60, window_senconds: int=60):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    current = await redis_client.incr(key)

    if current == 1:
        await redis_client.expire(key, window_senconds)

    if current > max_requests:
        raise HTTPException(
            status_code = status.HTTP_429_TOO_MANY_REQUESTS,
            detail = f"rate limit exceeded"
        )
