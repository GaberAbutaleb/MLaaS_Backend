from typing import Generic, Optional, TypeVar, Dict
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    username:str
    password:str

class SignupRequestSchema(BaseModel):
    username:str
    password:str
    email :str
    phone_number :str
    first_name :str
    last_name :str

class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T] = None
    
class TokenResponse(BaseModel):
    access_token :str
    token_type: str
