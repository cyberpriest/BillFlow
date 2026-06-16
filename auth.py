from fastapi.security import OAuth2PasswordBearer 
from passlib.context import CryptContext 
from fastapi import HTTPException,status,Depends
from jose import jwt,JWTError 
from sqlalchemy.orm import Session 
from datetime import datetime,timedelta,UTC
import os,database,models
from enums import Role
import secrets,string



bcrypt = CryptContext(schemes=['bcrypt'])
oauth2  = OAuth2PasswordBearer(tokenUrl='auth/login') 
TOKEN_EXPIRE_TIME = 60 * 24
SECRET_KEY = os.environ.get('SECRET_KEY','SECRET_KEY') 

def  hash_pwd(pwd:str)-> str:
    return  bcrypt.hash(pwd)


def  verify_pwd(plain_pwd:str,hash_pwd:str)->bool:
    return bcrypt.verify(plain_pwd,hash_pwd)


def encode_token(data:dict):
    encode_data = data.copy()
    payload = {'exp':datetime.now(tz = UTC) + timedelta(minutes=TOKEN_EXPIRE_TIME)}
    encode_data.update(payload)
    return jwt.encode(encode_data,SECRET_KEY,algorithm='HS256')


def decode_token(token:str):
    return jwt.decode(token,SECRET_KEY,algorithms=['HS256']) 

def generate_otp():
    return ''.join(secrets.choice(string.digits) for _ in range(5 ))

def authenticate(db:Session ,email :str,password:str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found ')
    
    if not verify_pwd(password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='invalid creds or wrong password')
    
    return user
    


def  get_current_user(token:str = Depends(oauth2),db:Session = Depends(database.get_db)):
    err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid authentication credentials',
        headers= {'WWW-Authenticate':'Bearer'}
    ) 

    try:

        payload = decode_token(token)

        email = payload.get('sub')
        if email is None:
            raise err 
    except JWTError :
        raise err 
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None :
        raise err 
    return user




def required_role(*role:Role):
    def check_role(user:models.User = Depends(get_current_user)):
        if user.role not in role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user 
    return check_role










