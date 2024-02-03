from datetime import datetime, timedelta

from fastapi import Response
from jose import jwt

from app.config import Config


async def create_and_set_access_token(user_id,
                                      response: Response):
    dct = dict()
    dct.update({'exp': datetime.utcnow() + timedelta(minutes=Config.jwt_token_expire_minutes)})
    dct.update({"sub": str(user_id)})
    token = jwt.encode(dct, key=Config.jwt_key, algorithm=Config.jwt_algorithm)
    response.set_cookie(key='Authorization', value=token, httponly=True)
