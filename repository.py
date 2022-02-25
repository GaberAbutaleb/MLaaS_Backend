from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from sqlalchemy import delete
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from model import ML_Model_Information

T = TypeVar('T')


class BaseRepo():

    @staticmethod
    def retrieve_all(db: Session, model: Generic[T]):
        return db.query(model).all()

    @staticmethod
    def retrieve_by_id(db: Session, model: Generic[T], id: int):
        return db.query(model).filter(model.id == id).all()

    @staticmethod
    def retrieve_by_ModuleCategory(db: Session, model: Generic[T], model_Category: str):
        return db.query(model).filter(model.model_Category == model_Category).all()


    @staticmethod
    def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)

    @staticmethod
    def update(db: Session, model: Generic[T]):
        db.commit()
        db.refresh(model)

    @staticmethod
    def delete(db: Session, model: Generic[T]):
        db.delete(model)
        db.commit()


class UsersRepo(BaseRepo):

    @staticmethod
    def find_by_username(db: Session, model: Generic[T], username: str):
        return db.query(model).filter(model.username == username).first()

    @staticmethod
    def delete_by_ids(db: Session,modelIds: List[int]):
        # db.query(model).filter(model.id.in_(modelIds)).delete()
        stmt = ( delete(ML_Model_Information).where(ML_Model_Information.id.in_(modelIds)))
        db.execute(stmt)
        db.commit()

class JWTRepo():

    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt

    def decode_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
            return decode_token if decode_token["expires"] >= datetime.time() else None
        except:
            return {}


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication sheme.")
            if self.verfity_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expiredd token.")
            return credentials.credentials
        else:
            raise HTTPException(
                status=403, detail="Invalid authorization code.")

    def verfity_jwt(Self, jwttoken: str):
        isTokenValid: bool = False

        try:
            payload = jwt.decode(jwttoken, SECRET_KEY, algorithm=[ALGORITHM])
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid
