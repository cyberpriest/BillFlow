from io import BytesIO
from sqlalchemy.orm import Session
from fastapi import  Depends, APIRouter
from fastapi.responses import StreamingResponse
import schema, auth, models

from database import get_db
from CRUD.invoicecrud import create_invoice, update_invoice, delete_invoice, get_invoice, all_invoice_list, generate_pdf

invoice_router = APIRouter(prefix='/invoice', tags=['INVOICE'])


@invoice_router.post('/add-invoice',response_model=schema.InvoiceResponse)
def add_invoice(data:schema.CreateInvoice,user:models.User = Depends(auth.get_current_user),db:Session = Depends(get_db)):
    return create_invoice(db, data, user)

@invoice_router.put('/update-invoice/{invoice_id}',response_model=schema.InvoiceResponse)
def patch_invoice(invoice_id: int, data: schema.InvoiceUpdate, user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return update_invoice(db, invoice_id, user, data)

@invoice_router.delete('/delete-invoice/{invoice_id}',response_model=schema.InvoiceResponse)
def remove_invoice(invoice_id: int, user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return delete_invoice(db, invoice_id, user)


@invoice_router.get('/get-invoice/{invoice_id}',response_model=schema.InvoiceResponse)
def getinvoice(invoice_id: int, user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return get_invoice(db, invoice_id, user)


@invoice_router.get('/all-invoices',response_model=schema.InvoiceResponsePagination)
def all_invoice(user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db), page: int = 1, limit: int = 10, search: str | None = None):
    return all_invoice_list(db, user, page, limit, search)


@invoice_router.get('/{invoice_id}/pdf')
def invoice_pdf(invoice_id: int, user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    pdf_bytes = generate_pdf(db, invoice_id, user)
    filename = f"invoice-{invoice_id}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type='application/pdf',
        headers={
            'Content-Disposition': f'inline; filename="{filename}"'
        }
    )

