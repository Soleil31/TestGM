from typing import Tuple

from app.core.security import create_access_token, create_refresh_token


async def create_tokens(user_id: int) -> Tuple[str, str]:
    access_token = await create_access_token(sub=str(user_id))
    refresh_token = await create_refresh_token(sub=str(user_id))

    return access_token, refresh_token
