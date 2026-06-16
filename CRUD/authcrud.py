
from sqlalchemy.orm import Session 
from fastapi import HTTPException,status
import schema,models,auth
from datetime import datetime,timedelta,UTC

from senduser_mail import send_email

def create_user(db:Session,email:str,password:str):
    user  = models.User(

       email = email,
       password = auth.hash_pwd(password)
        
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def request_otp(db:Session,data:schema.RequestOtp):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user : 
        user = models.User(
            email = data.email
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    #invalidate user otp 
    db.query(models.Otp)\
        .filter(models.Otp.owner_id == user.id,\
                models.Otp.is_used == False,\
                    ).delete(synchronize_session='fetch')
    db.commit()
    
    
    
    otp_code:str = str(auth.generate_otp())
    otp = models.Otp(
        code = otp_code,
        owner_id = user.id,
        expire_at = datetime.now(tz = UTC) + timedelta(minutes=60 * 24 )
    )
    db.add(otp)
    db.commit()
    # db.refresh(otp)
    try :
        send_email(email = user.email , code =  otp_code)
    except Exception as e:
        print(f"Error sending email: {e}")
    return {"message":'email sent '}



def verify_otp(db:Session , data:schema.VerifyOtp):
    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404,detail="invalid_code or user not found ")
    
    otp = db.query(models.Otp).filter(
        models.Otp.owner_id == user.id,
        models.Otp.is_used == False,
        models.Otp.expire_at > datetime.now(tz=UTC),
        models.Otp.code == data.code).first()
    if not otp:
        raise HTTPException(status_code=404,detail=" expired otp")
    otp.is_used = True 
    db.commit()

    return {'access_token':auth.encode_token({'sub':user.email}),'access_type':'bearer'}


