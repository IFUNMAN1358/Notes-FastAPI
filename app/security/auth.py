from fastapi import Request, Response, HTTPException
from jose import jwt, JWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import Config
from app.schemas import users
from app.postgres.crud import get_user_by_id
from app.security.JWT import create_and_set_access_token

# ================================================================
# Authorization function
# ================================================================


async def get_current_user(request: Request, response: Response):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = request.cookies.get('Authorization')
    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, Config.jwt_key, algorithms=[Config.jwt_algorithm])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(user_id=sub)
    if user is None:
        raise credentials_exception
    await create_and_set_access_token(user_id=user.id, response=response)
    return users.ReturnIdUser(id=user.id)
