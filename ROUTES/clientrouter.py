from  fastapi import APIRouter,Depends,status,HTTPException
import models,schema ,database,auth
from sqlalchemy.orm import  Session
from CRUD.clientcrud import create_client

client_router = APIRouter(prefix='/client',tags=['CLIENT'])

@client_router.post('/add-client',response_model=schema.ClientResponse)
def add_client(client_in:schema.CreateClient,
                business_id: int,
                user:models.User = Depends(auth.get_current_user),

               db:Session = Depends(database.get_db)):
    return create_client(db,business_id,user,client_in)


@client_router.patch('/update-client',response_model=schema.ClientResponse)
def update_client(client_id: int, data: schema.UpdateClient,
                  user: models.User = Depends(auth.get_current_user),
                  db: Session = Depends(database.get_db)):
    from CRUD.clientcrud import update_client as _update_client
    return _update_client(db, client_id, user, data)

@client_router.delete('/delete-client',response_model=schema.ClientResponse)
def delete_client(client_id: int, user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    from CRUD.clientcrud import delete_client as _delete_client
    return _delete_client(db, client_id, user)