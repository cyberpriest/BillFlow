from fastapi import APIRouter ,Depends,HTTPException ,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 
import database,models,schema,auth
from CRUD.authcrud import create_user,verify_otp,request_otp



auth_router  =  APIRouter(prefix='/auth',tags=['AUTHENTICATION'])

@auth_router.post('/request-otp')
def request_user_otp(data: schema.RequestOtp,db:Session = Depends(database.get_db)):
    return request_otp(db,data)

@auth_router.post('/verify-otp',response_model=schema.TokenResponse)
def verify_user_otp(data: schema.VerifyOtp,db:Session = Depends(database.get_db)):
    return verify_otp(db,data)


@auth_router.post('/register',response_model=schema.UserResponse)
def signup(user_in:schema.UserCreate,db:Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='this user already exist')
    return create_user(db,user_in.email,user_in.password)


@auth_router.post('/login',response_model=schema.TokenResponse)
def login(db:Session = Depends(database.get_db),data:OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    auth_user = auth.authenticate(db,email,password)
    user = db.query(models.User).filter(models.User.email == auth_user.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')

    token = auth.encode_token({'sub':user.email,'role':user.role})
    return {'access_token':token,'access_type':'bearer'}

