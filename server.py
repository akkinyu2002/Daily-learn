from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# --- Configuration ---
SECRET_KEY = "super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./secured_notes.db"

# --- Database Setup ---
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    salt = Column(String)
    nonce = Column(String)
    ciphertext = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class NoteBase(BaseModel):
    title: str
    salt: str
    nonce: str
    ciphertext: str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    updated_at: datetime
    class Config:
        from_attributes = True

# --- Security Helpers ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependencies ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# --- FastAPI App ---
app = FastAPI()

@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pwd = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/notes", response_model=List[NoteResponse])
def read_notes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Note).filter(Note.user_id == current_user.id).all()

@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = Note(**note.dict(), user_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes/{note_id}", response_model=NoteResponse)
def read_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    for var, value in vars(note).items():
        setattr(db_note, var, value)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)