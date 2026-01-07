from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from fast_agend.schemas import Message, UserSchema, UserPublic, UserDB, UserList
from sqlalchemy.orm import Session
from fast_agend.models import User
from fast_agend.core.deps import get_db

app = FastAPI(title='Backend do App de Agendamento')

database = []

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!!!'}

@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}


@app.put("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    db.commit()
    db.refresh(db_user)

    return db_user

@app.delete("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado"
        )

    db.delete(db_user)
    db.commit()

    return db_user