

# Response fields: total_clients,
# total_invoices, total_paid, total_unpaid,
# revenue_month, revenue_year, overdue_count, 
# upcoming_due, trend (array of {month, revenue}),
# top_clients (array), recent_invoices (array).


from sqlalchemy.orm  import Session 
import models 
from enums import InvoiceStatus
from sqlalchemy import func

from datetime import datetime ,UTC
now = datetime.now(tz= UTC)

def dashboard(db:Session,user:models.User):
    total_clients = (
        db.query(func.count(func.distinct(models.Invoice.client_id))) 
        .join(models.Business).filter(
            models.Business.owner_id  == user.id

        ).scalar()
    ) 
    total_invoices = (
        db.query(func.coalesce(func.sum(models.Invoice.total))) 
        .join(models.Business).filter(
            models.Business.owner_id  == user.id

        ).scalar()
    ) 

    total_paid = (
        db.query(func.coalesce(func.sum(models.Invoice.total),0)) 
        .join(models.Business).filter(
            models.Business.owner_id  == user.id,
            models.Invoice.status == InvoiceStatus.paid

        ).scalar()
    ) 

    total_unpaid = (
        db.query(func.coalesce(func.sum(models.Invoice.total),0))\
            .join(models.Business).filter(
                models.Invoice.status == InvoiceStatus.overdue,
                models.Business.owner_id == user.id
            ).scalar()

        )
    revenue_year = (
        db.query(func.coalesce(func.sum(models.Invoice.total),0)).\
            join(models.Business)\
                .filter(
                models.Invoice.status == InvoiceStatus.paid,
                models.Business.owner_id == user.id,
                func.extract('month',models.Invoice.due_date) == now.month,
                func.extract('year',models.Invoice.due_date) == now.year

            ).scalar()


    )

    revenue_month = (
        db.query(func.coalesce(func.sum(models.Invoice.total),0)).\
            join(models.Business)\
                .filter(
                models.Invoice.status == InvoiceStatus.paid,
                models.Business.owner_id == user.id,
                func.extract('month',models.Invoice.due_date) == now.month,

            ).scalar()


    )

    trend = ( 

        db.query(


        )



    )

    

    
    
