from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import auth, models, schema
from database import get_db
from CRUD.dashboard import dashboard


dashboard_router = APIRouter(prefix='/dashboard', tags=['DASHBOARD'])


@dashboard_router.get('/', response_model=schema.DashboardResponse)
def get_dashboard(user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return dashboard(db, user)
