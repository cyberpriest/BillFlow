from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException,status
import enums
import database, models, schema, auth
from CRUD.businesscrud import create_business, update_business, remove_business, get_all_business_list,get_business_id

business_router = APIRouter(prefix='/business', tags=['BUSINESS'])


@business_router.get('/', response_model=schema.BusinessResponse)
def list_businesses(page:int=1,
                    limit:int = 10, 
                    search:str|None = None,
                    db: Session = Depends(database.get_db),
                    user: models.User = Depends(auth.required_role(enums.Role.admin,enums.Role.developer))):
    return get_all_business_list(db, user,page,limit,search)

@business_router.get('/{business_id}', response_model=schema.Business)
def get_business(business_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(auth.get_current_user)):
    business = get_business_id(db, business_id, user)
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='business not found or you are not the owner')
    return business


@business_router.post('/', response_model=schema.Business)
def create_business_route(business_in: schema.CreateBusiness, db: Session = Depends(database.get_db), user: models.User = Depends(auth.get_current_user)):
    return create_business(db, business_in, user)


@business_router.put('/{business_id}', response_model=schema.Business)
def update_business_route(business_id: int, business_in: schema.CreateBusiness, db: Session = Depends(database.get_db), user: models.User = Depends(auth.get_current_user)):
    return update_business(db, business_id, business_in, user)


@business_router.delete('/{business_id}')
def remove_business_route(business_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(auth.get_current_user)):
    return remove_business(db, business_id, user)
