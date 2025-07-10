from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas, database
from app.auth import create_access_token, verify_password, get_current_user

Base = database.Base
engine = database.engine
SessionLocal = database.SessionLocal
get_db = database.get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/contacts/", response_model=schemas.ContactOut)
def create(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

@app.get("/contacts/", response_model=list[schemas.ContactOut])
def read_contacts(db: Session = Depends(get_db)):
    return crud.get_contacts(db)

@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    updated = crud.update_contact(db, contact_id, contact)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated

@app.delete("/contacts/{contact_id}")
def delete(contact_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": f"Контакт {contact_id} удалён"}

# Авторизация (JWT)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


