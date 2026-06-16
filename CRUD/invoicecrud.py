from fastapi import HTTPException, status 
from sqlalchemy.orm import Session
import models, schema, enums
from pagination import Pagination
from generate_pdf import render_invoice_pdf






def create_invoice(db:Session,data:schema.CreateInvoice,user:models.User):
    is_authorized = user.role in [enums.Role.admin,enums.Role.developer,enums.Role.staff]

    if not is_authorized:
        raise HTTPException(status_code=404,detail="Not authorized to access this resource")
    

    buisness = db.query(models.Business).filter(
        models.Business.id == data.business_id ,
        models.Business.owner_id == user.id
        ).first()
    
    if not buisness:
        raise HTTPException(status_code=404,detail="Buissness not found")
    
    clients = db.query(models.Client).join(models.Business).filter(
        models.Client.id == data.client_id,
        models.Business.owner_id == user.id
     ).first()
    

    
    if not clients:
        raise HTTPException(status_code=404,detail="client not found")
    
    add_invoice = models.Invoice(
        **data.model_dump()
    )
    db.add(add_invoice)
    db.flush() 

    total:float = 0.0

    for  item  in data.items:
        invoice_item = models.InvoiceItem(
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            invoice_id=add_invoice.id
        )
        total += item.quantity * item.unit_price
        db.add(invoice_item)



    add_invoice.total = total 
    db.commit()
    db.refresh(add_invoice)
    return add_invoice







def update_invoice(db:Session,invoice_id:int,user:models.User,data:schema.InvoiceUpdate):
    inv = db.query(models.Invoice).join(models.Business).filter(
        models.Invoice.id == invoice_id,
        models.Business.owner_id == user.id).first()
    if not inv:
        raise HTTPException(status_code=404,detail="invoice not found")
    
    for k,v in data.model_dump(exclude_unset=True).items():
        setattr(inv,k,v)


def delete_invoice(db:Session,invoice_id:int,user:models.User):
    inv = db.query(models.Invoice).join(models.Business).filter(
        models.Invoice.id == invoice_id,
        models.Business.owner_id == user.id).first()
    if not inv:
        raise HTTPException(status_code=404,detail="invoice not found")
    db.delete(inv)
    db.commit()


def get_invoice(db:Session,invoice_id:int,user:models.User):
    inv = db.query(models.Invoice).join(models.Business).filter(
        models.Invoice.id == invoice_id,
        models.Business.owner_id == user.id).first()
    if not inv:
        raise HTTPException(status_code=404,detail="invoice not found")
    return inv

def all_invoice_list(db:Session,user:models.User,page:int = 1,limit:int = 10,search:str|None = None):
    is_authorized = user.role in [enums.Role.admin,enums.Role.developer,enums.Role.staff]
    if not is_authorized:
        raise HTTPException(status_code=403,detail="Not authorized to access this resource")
    query = db.query(models.Invoice).join(models.Business).filter(
        models.Business.owner_id == user.id
    )
    if search:
        query = query.filter(models.Invoice.name.ilike(f'%{search}%'))
    
    total_clients = query.count()
    page,limit = Pagination(page,limit)
    result = query.order_by(models.Invoice.issue_date.desc()).offset(page).limit(limit).all()
    return {   
        'result':result,
        'limit':limit,
        'page':page,
        'total':total_clients
     }


### Phase 5 — Status & Business Logic
# - [ ] `POST /invoices/{id}/send` — mark as sent (status: draft → sent)
# - [ ] `POST /invoices/{id}/mark-paid` — mark as paid (status: sent → paid)
# - [ ] `POST /invoices/{id}/mark-overdue` — mark as overdue (status: sent → overdue)

def send_inv(db:Session,status:str,invoice_id:int,user:models.User):
    inv = db.query(models.Invoice).join(models.Business).filter(
        models.Invoice.id == invoice_id,
        models.Business.owner_id == user.id).first()
    if not inv:
        raise HTTPException(status_code=404,detail="invoice not found")
    if status == 'send' and inv.status == enums.InvoiceStatus.draft:
        inv.status = enums.InvoiceStatus.sent
    elif status == 'mark-paid' and inv.status == enums.InvoiceStatus.sent:
        inv.status = enums.InvoiceStatus.paid
    elif status == 'overdue' and inv.status == enums.InvoiceStatus.sent:
        inv.status = enums.InvoiceStatus.overdue
    else:
        raise HTTPException(status_code=400,detail="Invalid status transition")
    
    db.commit()
    db.refresh(inv)
    return inv

### Phase 7 — PDF Export (stretch goal)
# - [ ] `GET /invoices/{id}/pdf` — generate and return a PDF of the invoice
# - [ ] Use `reportlab`

def generate_pdf(db:Session,id:int,user:models.User):
    inv = db.query(models.Invoice).join(models.Business).filter(
        models.Invoice.id == id,
        models.Business.owner_id == user.id
    ).first()

    if not inv:
        raise HTTPException(status_code=404,detail='invoice not found')

    return render_invoice_pdf(inv)
