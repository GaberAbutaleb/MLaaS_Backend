from typing import Generic, Optional, TypeVar, Dict
from pydantic.generics import GenericModel
from pydantic import BaseModel, Field
from typing import List

T = TypeVar('T')


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    username:str
    password:str

class MLModInfoReq(BaseModel):
    model_Category :str
    model_used :str
    deployment_Model_Name :str
    Model_Output_File_Name :str

class PredictClustringModel(BaseModel):
    modelName: str
    predictList: List[float]
    modelUsed: str

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
