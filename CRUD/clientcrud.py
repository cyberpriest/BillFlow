
from sqlalchemy.orm import Session 
import models,schema,enums
from fastapi import HTTPException,status
from pagination import Pagination






def create_client(db:Session,business_id:int,user:models.User,data:schema.CreateClient):
    business = db.query(models.Business).filter(
        models.Business.id == business_id,
        models.Business.owner_id == user.id
        ).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='business not found or you are not the owner')
    client = models.Client(

        business_id = business_id,
        **data.model_dump()

        )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def update_client(db:Session,client_id:int,user:models.User,data:schema.UpdateClient):
    client = db.query(models.Client).join(models.Business).filter(
        models.Client.id == client_id,
        models.Business.owner_id == user.id
    ).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='client not found or you are not the owner')
    
    for k,v in data.model_dump(exclude_unset=True).items():
        setattr(client,k,v)
    db.commit()
    db.refresh(client)
    return client


def delete_client(db:Session,client_id:int,user:models.User):
    client = db.query(models.Client).join(models.Business).filter(
        models.Client.id == client_id,
        models.Business.owner_id == user.id
    ).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='client not found or you are not the owner')
    
    db.delete(client)
    db.commit()
    return {'message':'client deleted sucessfully'}

def get_all_client_list(db:Session,page:int = 1,limit:int = 10,search:str|None = None):

    query = db.query(models.Client)
    if search:
        query.filter(models.Client.client_name.ilike(f"%{search}%"))
    total_clients = query.count()
    page,limit = Pagination(page,limit)

    result =  query.offset(page).limit(limit).all()
    return {
        'result':result,
        'page':page,
        'limit':limit,
        'total':total_clients,

        }
