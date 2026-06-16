from  fastapi import APIRouter,Depends,status,HTTPException
import models,schema 
from sqlalchemy.orm import  Session
from CRUD.clientcrud import create_client

client_router = APIRouter(prefix='/client',tags=['CLIENT'])

@client_router.post('/add-client',response_model=schema.ClientResponse)
def add_client():
    pass


@client_router.patch('/update-client',response_model=schema.ClientResponse)
def update_client():
    pass 

@client_router.delete('/delete-client',response_model=schema.ClientResponse)
def delete_client():
    pass