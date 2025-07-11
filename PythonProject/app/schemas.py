from pydantic import BaseModel

class ContactBase(BaseModel):
    name: str
    phone: str

class ContactCreate(ContactBase):
    pass

class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True



from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
