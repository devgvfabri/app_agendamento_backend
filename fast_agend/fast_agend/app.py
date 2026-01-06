from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fast_agend.schemas import Message, UserSchema, UserPublic, UserDB, UserList


app = FastAPI(title='Backend do App de Agendamento')

database = []

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!!!'}

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        username = user.username,
        email = user.email,
        password = user.password,
        id = len(database) + 1
    )
    database.append(user_with_id)
    return user_with_id

@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(
        username = user.username,
        email = user.email,
        password = user.password,
        id = user_id
    )
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim não achei!') 
    database[user_id - 1] = user_with_id
    return user_with_id

@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Deu ruim não achei!') 
    return database.pop(user_id - 1)


