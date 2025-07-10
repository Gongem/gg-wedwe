from sqlalchemy.orm import Session
from app.models import Contact
from app.schemas import ContactCreate

def get_contacts(db: Session):
    return db.query(Contact).all()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(name=contact.name, phone=contact.phone)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def delete_contact(db: Session, contact_id: int):
    contact = get_contact_by_id(db, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact

def update_contact(db: Session, contact_id: int, contact_data: ContactCreate):
    contact = get_contact_by_id(db, contact_id)
    if contact:
        contact.name = contact_data.name
        contact.phone = contact_data.phone
        db.commit()
        db.refresh(contact)
    return contact

from app import models, schemas
from sqlalchemy.orm import Session
from app.auth import get_password_hash

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
