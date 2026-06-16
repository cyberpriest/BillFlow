from fastapi import  FastAPI,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ROUTES.authroute import auth_router
from ROUTES.businessrouter import business_router
from ROUTES.clientrouter import client_router
from ROUTES.invoicerouter import invoice_router


from database import engine,Base
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from ROUTES.clientrouter import client_router
limiter = Limiter(key_func=get_remote_address)



app = FastAPI(title="Invoice Manager",description="A simple invoice management system built with FastAPI and SQLAlchemy for small businesses to create and manage invoices efficiently.")
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://id-preview--e2c2611d-8944-43e6-a519-8fdb21921a6e.lovable.app"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded,)




app.include_router(auth_router)
app.include_router(business_router)
app.include_router(client_router)
app.include_router(invoice_router)

Base.metadata.create_all(bind=engine)