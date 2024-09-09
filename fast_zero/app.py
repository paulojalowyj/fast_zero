from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, users
from fast_zero.schemas import Message

app = FastAPI(title='FastAPI from Zero', description='A FastAPI Boilerplate')

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Batatinha Frita 123'}
