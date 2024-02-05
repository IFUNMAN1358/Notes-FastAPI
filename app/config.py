from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Config:
    __DB_USER = getenv('DB_USER')
    __DB_PASSWORD = getenv('DB_PASSWORD')
    __DB_HOST = getenv('DB_HOST')
    __DB_PORT = getenv('DB_PORT')
    __DB_NAME = getenv('DB_NAME')

    # url for connect to database postgres
    postgres_url =\
        f'postgresql+asyncpg://{__DB_USER}:{__DB_PASSWORD}@{__DB_HOST}:{__DB_PORT}/{__DB_NAME}?async_fallback=True'

    # data for jwt authentication
    jwt_key = getenv('JWT_KEY')
    jwt_algorithm = getenv('JWT_ALGORITHM')
    jwt_token_expire_minutes = int(getenv('JWT_TOKEN_EXPIRE_MINUTES'))
