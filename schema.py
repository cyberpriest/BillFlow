from pydantic import BaseModel
from typing import Optional

from datetime  import  datetime

class UserBase(BaseModel):
    email:str 
    # fullname:Optional[str] = None
    password:str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email:Optional[str] = None 
    fullname:Optional[str] = None

class UserResponse(BaseModel):
    id:int
    email:str

    class Config():
        from_attributes = True



class TokenResponse(BaseModel):
    access_token:str
    access_type:str = 'bearer'
    

class RequestOtp(BaseModel):
    email:str


class VerifyOtp(BaseModel):
    email:str
    code :str


class BusinessBase(BaseModel):
    business_name:str
    business_email:str
    address:str
    phone:str


class CreateBusiness(BusinessBase):
    pass


class Business(BaseModel):
    id:int
    owner_id:int
    business_name:str
    business_email:str
    address:str
    phone:str


    class Config:
        from_attributes = True

class BusinessResponse(BaseModel):
    
    page:int
    limit:int
    total:int
    result : list[Business] 


class Client(BaseModel):
    id:int
    client_name:str
    client_email:str
    address:str
    phone:str
    business_id:int




class CreateClient(Client):
    client_name:str
    client_email:str
    address:str
    phone:str

class UpdateClient(BaseModel):
    client_name:Optional[str] = None
    client_email:Optional[str] = None
    address:Optional[str] = None
    phone:Optional[str] = None



class ClientResponse(Client):
    id:int
    business_id:int
    class Config:
        from_attributes = True


class InvoiceItems(BaseModel):
    description:str
    quantity:float
    unit_price:float





class Invoice(BaseModel):
    id:int
    business_id:int
    client_id:int
    due_date:datetime|None = None
    items:list[InvoiceItems]
    # name:Optional[str] = None
    # description:Optional[str] = None
    # amount:Optional[float] = None




class CreateInvoice(Invoice):
    pass

class InvoiceUpdate(BaseModel):
    name:Optional[str] = None
    description:Optional[str] = None
    amount:Optional[float] = None



class InvoiceResponse(Invoice):
    id:int
    business_id:int
    client_id:int

    class Config:
        from_attributes = True

class InvoiceResponsePagination(BaseModel):
    result:list[InvoiceResponse] = []
    total:int
    page:int
    limit:int


class DashboardTrend(BaseModel):
    month:int
    revenue:float

    class Config:
        from_attributes = True


class DashboardClient(BaseModel):
    client_id:int
    client_name:str
    revenue:float

    class Config:
        from_attributes = True


class DashboardInvoiceSummary(BaseModel):
    id:int
    invoice_no:str
    status:str
    total:float
    due_date:Optional[datetime] = None

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    total_clients:int
    total_invoices:float
    total_paid:float
    total_unpaid:float
    revenue_month:float
    revenue_year:float
    overdue_count:int
    upcoming_due:int
    trend:list[DashboardTrend] = []
    top_clients:list[DashboardClient] = []
    recent_invoices:list[DashboardInvoiceSummary] = []

    class Config:
        from_attributes = True


class InvoiceItem(BaseModel):
    id:int
    invoice_id:int
    description:str
    quantity:float
    unit_price:float