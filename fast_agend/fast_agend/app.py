from http import HTTPStatus
from fastapi import FastAPI
from fast_agend.schemas import Message


app = FastAPI(title='Backend do App de Agendamento')

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!!!'}
