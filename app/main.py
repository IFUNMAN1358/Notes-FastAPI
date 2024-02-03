from fastapi import FastAPI

from app.routers.account import router as account_router
from app.routers.notes import router as notes_router

app = FastAPI()


app.include_router(
    router=account_router,
    prefix='/account',
    tags=['Account']
)


app.include_router(
    router=notes_router,
    prefix='/notes',
    tags=['Notes']
)
