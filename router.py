from fastapi import APIRouter, Depends, Request
from schema import RequestSchema, ResponseSchema,SignupRequestSchema, TokenResponse,MLModInfoReq
from sqlalchemy.orm import Session
from config import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from repository import JWTRepo, JWTBearer, UsersRepo
from model import Users,ML_Model_Information
from jose import jwt
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
    Authentication Router

"""


@router.post('/signup')
async def signup(request: SignupRequestSchema, db: Session = Depends(get_db)):
    try:
        # insert user to db
        _user = Users(username=request.username,
                      email=request.email,
                      phone_number=request.phone_number,
                      password=pwd_context.hash(
                          request.password),
                      first_name=request.first_name,
                      last_name=request.last_name)
        UsersRepo.insert(db, _user)
        return ResponseSchema(code="200", status="Ok", message="Success save data").dict(exclude_none=True)
    except Exception as error:
        print(error.args)
        return ResponseSchema(code="500", status="Error", message="Internal Server Error").dict(exclude_none=True)


@router.post('/login')
async def login(request: RequestSchema, db: Session = Depends(get_db)):
    try:
       # find user by username
        print(request)
        _user = UsersRepo.find_by_username(
            db, Users, request.username)
        if not pwd_context.verify(request.password, _user.password):
            return ResponseSchema(code="400", status="Bad Request", message="Invalid password").dict(exclude_none=True)

        token = JWTRepo.generate_token({"userName": _user.username,"roles":"Admin#manager"})
        return ResponseSchema(code="200", status="OK", message="success login!", result=TokenResponse(access_token=token, token_type="Bearer")).dict(exclude_none=True)
    except Exception as error:
        error_message = str(error.args)
        print(error_message)
        return ResponseSchema(code="500", status="Internal Server Error", message="Internal Server Error").dict(exclude_none=True)


"""
    Users Router

"""


@router.get("/users", dependencies=[Depends(JWTBearer())])
async def retrieve_all(request: Request,db: Session = Depends(get_db)):
    token = request.headers.get('Authorization').replace("Bearer ", "")
    print(token)
    payload = jwt.decode(token, key='lemoncode21', options={"verify_signature": False})
    print (payload["userName"])
    _user = UsersRepo.retrieve_all(db, Users)
    return ResponseSchema(code="200", status="Ok", message="Sucess retrieve data", result=_user).dict(exclude_none=True)


@router.get("/userModelsInformation", dependencies=[Depends(JWTBearer())])
async def retrieve_userModelsInformation(request: Request, model_Category: str,db: Session = Depends(get_db)):
    token = request.headers.get('Authorization').replace("Bearer ", "")
    payload = jwt.decode(token, key='lemoncode21', options={"verify_signature": False})
    print (payload["userName"])
    # _userInfo = UsersRepo.retrieve_by_ModuleCategory(db, ML_Model_Information,model_Category)
    _userInfo = UsersRepo.retrieve_all(db, ML_Model_Information)
    return ResponseSchema(code="200", status="Ok", message="Sucess retrieve data", result=_userInfo).dict(exclude_none=True)


@router.post("/InsertuserModelsInfo", dependencies=[Depends(JWTBearer())])
async def InsertuserModelsInfo(request: Request,mlModelInfoObj : MLModInfoReq ,db: Session = Depends(get_db)):
    token = request.headers.get('Authorization').replace("Bearer ", "")
    payload = jwt.decode(token, key='lemoncode21', options={"verify_signature": False})
    username = payload["userName"]
    print(mlModelInfoObj)
    _MLM_Info = ML_Model_Information(username=username,
                  model_Category=mlModelInfoObj.model_Category,
                  model_used=mlModelInfoObj.model_used,
                  deployment_Model_Name =mlModelInfoObj.deployment_Model_Name,
                  Model_Output_File_Name = mlModelInfoObj.Model_Output_File_Name)
    _userModelInfo = UsersRepo.insert(db, _MLM_Info)
    return ResponseSchema(code="200", status="Ok", message="Sucess saved data", result=_userModelInfo).dict(exclude_none=True)

@router.delete("/deleteuserModelsInfo/{modelIds}", dependencies=[Depends(JWTBearer())])
async def InsertuserModelsInfo( modelIds: str,db: Session = Depends(get_db)):
    print(modelIds)
    string_list = modelIds.split(",")
    intIdList = list(map(int, string_list))
    mL_Model_Information = ML_Model_Information()
    _userModelInfo = UsersRepo.delete_by_ids(db,intIdList)
    return ResponseSchema(code="200", status="Ok", message="Sucess saved data", result=_userModelInfo).dict(exclude_none=True)
