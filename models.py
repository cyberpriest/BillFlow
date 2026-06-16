from database import Base
from  sqlalchemy.orm  import Mapped,mapped_column,relationship
from sqlalchemy import String,DateTime,Enum ,ForeignKey,Integer,Float,Boolean
from datetime import datetime, timezone,UTC
from uuid import uuid4

from enums import Plan, Role,InvoiceStatus

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True,index=True) 
    email :Mapped[str] = mapped_column(String(10),nullable =  False ,unique=True,index=True)
    fullname : Mapped[str] = mapped_column(String(10),nullable =  True ,index=True)
    role :Mapped[Role] = mapped_column(Enum(Role),default = Role.admin,nullable =  False ,index=True)
    plan :Mapped[Plan] = mapped_column(Enum(Plan),default = Plan.free,nullable =  False ,index=True)

    shop_owner : Mapped[str] = mapped_column(String(10),nullable =  True ,index=True)
    password : Mapped[str] = mapped_column(String(255),nullable =  False )
    created_at : Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc),nullable =  False )
    business :Mapped[list['Business']] = relationship('Business',back_populates='owner')
    otp :Mapped[list['Otp']] = relationship('Otp',back_populates='owner')




class Otp(Base):
    __tablename__ = 'otp'
    id: Mapped[int] = mapped_column(primary_key=True)
    code :Mapped[str] = mapped_column(String , nullable=False)
    owner_id :Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(tz= UTC))
    is_used:Mapped[bool] = mapped_column(Boolean ,default=False)
    expire_at :Mapped[datetime] = mapped_column(DateTime,nullable=True)
    owner : Mapped['User'] = relationship('User',back_populates='otp')


class Business(Base):
    __tablename__ = 'business'
    id:Mapped[int] = mapped_column(primary_key=True,index=True) 
    business_name :Mapped[str] = mapped_column(String(10),nullable =  False ,index=True)
    business_email :Mapped[str] = mapped_column(String(10),nullable =  False ,index=True)
    address : Mapped[str] = mapped_column(String(255),nullable =  False )
    phone : Mapped[str] = mapped_column(String(20),nullable =  False )
    owner_id : Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    owner : Mapped['User'] = relationship('User',back_populates='business')
    clients : Mapped[list['Client']] = relationship('Client',back_populates='business') 
    invoices : Mapped[list['Invoice']] = relationship('Invoice',back_populates='business')




class Client(Base):
    __tablename__ = 'client'
    id:Mapped[int] = mapped_column(primary_key=True,index=True) 
    client_name :Mapped[str] = mapped_column(String(10),nullable =  False ,index=True)
    client_email :Mapped[str] = mapped_column(String(10),nullable =  False ,index=True)
    address : Mapped[str] = mapped_column(String(255),nullable =  False )
    phone : Mapped[str] = mapped_column(String(20),nullable =  False )
    business_id : Mapped[int] = mapped_column(Integer,ForeignKey('business.id'),nullable=False)
    business : Mapped['Business'] = relationship('Business',back_populates='clients')
    invoices : Mapped[list['Invoice']] = relationship('Invoice',back_populates='client')



class Invoice(Base):
    __tablename__ = 'invoice'
    id:Mapped[int] = mapped_column(primary_key=True,index=True) 

    client_id:Mapped[int] =  mapped_column(Integer,ForeignKey('client.id'))
    business_id:Mapped[int] = mapped_column(Integer,ForeignKey('business.id'))

    invoice_no:Mapped[str] = mapped_column(String,default=lambda: 'INV-' + uuid4().hex[:5])
    status:Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus),default=InvoiceStatus.draft)
    issue_date:Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc),nullable=False)
    due_date : Mapped[datetime] = mapped_column(DateTime,nullable=True)
    client : Mapped['Client'] = relationship('Client',back_populates='invoices')
    business : Mapped['Business'] = relationship('Business',back_populates='invoices')
    total: Mapped[float] = mapped_column(Float, default=0.0)

    items : Mapped[list['InvoiceItem']] = relationship('InvoiceItem', back_populates='invoice')





class InvoiceItem(Base):
    __tablename__ = 'invoiceitem'
    id:Mapped[int] = mapped_column(primary_key=True,index=True) 
    invoice_id : Mapped[int]  =  mapped_column(Integer,ForeignKey('invoice.id'))
    description : Mapped[str] = mapped_column(String(255),nullable =  False )
    quantity: Mapped[float]  =  mapped_column(Float,nullable=False)
    unit_price:Mapped[float]  =  mapped_column(Float,nullable=False)
    invoice : Mapped['Invoice'] = relationship('Invoice',back_populates='items')
    








