from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from app.postgres.crud import get_user_by_id, get_user_by_email_or_username
from app.postgres.engine import get_db
from app.postgres.tables import User
from app.schemas import users
from app.security.JWT import create_and_set_access_token
from app.security.password import hash_password, verify_password
from app.security.auth import get_current_user

router = APIRouter()


@router.post('/registration', response_model=users.ReturnIdUser, status_code=201)
async def create_user(user_data: users.RegisterUser,
                      db: AsyncSession = Depends(get_db)):
    if await db.scalar(select(User).where(or_(User.username == user_data.username, User.email == user_data.email))):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='User with this username or email already exist!'
        )
    user = User(username=user_data.username,
                email=user_data.email,
                hashed_password=hash_password(user_data.password))
    db.add(user)
    await db.commit()
    return users.ReturnIdUser(id=user.id)


@router.delete('/delete_account', response_model=users.ReturnIdUser, status_code=200)
async def delete_user(db: AsyncSession = Depends(get_db),
                      current_user: users.ReturnIdUser = Depends(get_current_user)):
    user = await get_user_by_id(user_id=current_user.id)
    await db.delete(user)
    await db.commit()
    return users.ReturnIdUser(id=current_user.id)


@router.post('/login', status_code=202)
async def login_user(response: Response,
                     form_data: users.LoginUser):
    user = await get_user_by_email_or_username(form_data.email_username)
    if user is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='User with this email or username not exist!'
        )
    if not verify_password(plained_password=form_data.password,
                           hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Wrong password!'
        )
    await create_and_set_access_token(user_id=user.id, response=response)
    return {'status': 'Login is successful'}


@router.post('/logout', status_code=205)
async def logout(response: Response,
                 current_user: users.ReturnIdUser = Depends(get_current_user)):
    response.delete_cookie(key='Authorization')
    return {'status': 'Logout is successful'}
