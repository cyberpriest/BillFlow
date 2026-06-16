
from sqlalchemy.orm import Session 
import models,schema,enums
from fastapi import HTTPException,status
from check_plan_limit import check_limit
from pagination import Pagination

def get_business_id(db:Session,business_id:int,user:models.User):
    b = db.query(models.Business).filter(models.Business.id == business_id, models.Business.owner_id == user.id).first()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='business not found or you are not the owner')


def get_all_business_list(db:Session,user:models.User,page:int = 1,limit:int = 10,search:str|None = None):

    query = db.query(models.Business).filter(models.Business.owner_id == user.id)
    if search:
        query = query.filter(models.Business.name.ilike(f'%{search}%'))
    
    total_clients = query.count()
    pages,limits = Pagination(page,limit)
    result = query.order_by(models.Business.id.desc()).offset(pages).limit(limits).all()
    return {   
        
        'limit':limits,
        'page':pages,
        'total':total_clients,
        'result':result}

def create_business(db:Session,business_data:schema.CreateBusiness,user:models.User):
    check_limit(db, user)
    business = models.Business(
        **business_data.model_dump(),
        owner_id = user.id)
    db.add(business)
    db.commit()
    db.refresh(business)
    return business 


def update_business(db:Session,update_id:int,business_data:schema.CreateBusiness,user:models.User):
    business = get_business_id(db,update_id,user)
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='business not found ')
    
    is_user =  user.id == business.owner_id
    is_authorized = user.role in  [enums.Role.admin,enums.Role.developer]

    if not( is_user or  is_authorized):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = 'sorry not authorized')
    
    for k,v in business_data.model_dump(exclude_unset=True).items():
        setattr(business,k,v)
    db.commit()
    db.refresh(business)
    return business



def remove_business(db:Session,delete_id:int,user:models.User):
    business = get_business_id(db,delete_id,user)
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='business not found ')
    
    is_user =  user.id == business.owner_id
    is_authorized = user.role in  [enums.Role.admin,enums.Role.developer]

    if not( is_user or  is_authorized):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = 'sorry not authorized')
    db.delete(business)
    db.commit()
    return {'message':'deleted sucessfully'}
    


    

    

