from datetime import datetime, timedelta, UTC

from sqlalchemy import func
from sqlalchemy.orm import Session

import models
from enums import InvoiceStatus


def dashboard(db: Session, user: models.User):
    now = datetime.now(tz=UTC)
    next_week = now + timedelta(days=7)

    total_clients = (
        db.query(func.count(func.distinct(models.Invoice.client_id)))
        .join(models.Business)
        .filter(models.Business.owner_id == user.id)
        .scalar()
    ) or 0

    total_invoices = (
        db.query(func.coalesce(func.sum(models.Invoice.total), 0.0))
        .join(models.Business)
        .filter(models.Business.owner_id == user.id)
        .scalar()
    ) or 0.0

    total_paid = (
        db.query(func.coalesce(func.sum(models.Invoice.total), 0.0))
        .join(models.Business)
        .filter(
            models.Business.owner_id == user.id,
            models.Invoice.status == InvoiceStatus.paid,
        )
        .scalar()
    ) or 0.0

    total_unpaid = (
        db.query(func.coalesce(func.sum(models.Invoice.total), 0.0))
        .join(models.Business)
        .filter(
            models.Business.owner_id == user.id,
            models.Invoice.status != InvoiceStatus.paid,
        )
        .scalar()
    ) or 0.0

    revenue_month = (
        db.query(func.coalesce(func.sum(models.Invoice.total), 0.0))
        .join(models.Business)
        .filter(
            models.Business.owner_id == user.id,
            models.Invoice.status == InvoiceStatus.paid,
            func.extract('month', models.Invoice.due_date) == now.month,
            func.extract('year', models.Invoice.due_date) == now.year,
        )
        .scalar()
    ) or 0.0

    revenue_year = (
        db.query(func.coalesce(func.sum(models.Invoice.total), 0.0))
        .join(models.Business)
        .filter(
            models.Business.owner_id == user.id,
            models.Invoice.status == InvoiceStatus.paid,
            func.extract('year', models.Invoice.due_date) == now.year,
        )
        .scalar()
    ) or 0.0

    overdue_count = (
        db.query(func.count(models.Invoice.id))
        .join(models.Business)
        .filter(
            models.Business.owner_id == user.id,
            models.Invoice.status == InvoiceStatus.overdue,
        )
        .scalar()
    ) or 0

    upcoming_due = (
        db.query(func.count(models.Invoice.id))
        .join(models.Business)
        .filter(
            models.Business.owner_id == user.id,
            models.Invoice.status != InvoiceStatus.paid,
            models.Invoice.due_date != None,
            models.Invoice.due_date >= now,
            models.Invoice.due_date <= next_week,
        )
        .scalar()
    ) or 0

    trend_rows = (
        db.query(
            func.extract('month', models.Invoice.due_date).label('month'),
            func.coalesce(func.sum(models.Invoice.total), 0.0).label('revenue'),
        )
        .join(models.Business)
        .filter(
            models.Business.owner_id == user.id,
            models.Invoice.status == InvoiceStatus.paid,
            func.extract('year', models.Invoice.due_date) == now.year,
        )
        .group_by('month')
        .order_by('month')
        .all()
    )

    top_clients_rows = (
        db.query(
            models.Client.id.label('client_id'),
            models.Client.client_name.label('client_name'),
            func.coalesce(func.sum(models.Invoice.total), 0.0).label('revenue'),
        )
        .join(models.Client)
        .join(models.Business)
        .filter(
            models.Business.owner_id == user.id,
            models.Invoice.status == InvoiceStatus.paid,
        )
        .group_by(models.Client.id, models.Client.client_name)
        .order_by(func.sum(models.Invoice.total).desc())
        .limit(5)
        .all()
    )

    recent_invoices_rows = (
        db.query(
            models.Invoice.id,
            models.Invoice.invoice_no,
            models.Invoice.status,
            models.Invoice.total,
            models.Invoice.due_date,
        )
        .join(models.Business)
        .filter(models.Business.owner_id == user.id)
        .order_by(models.Invoice.issue_date.desc())
        .limit(5)
        .all()
    )

    return {
        'total_clients': int(total_clients),
        'total_invoices': float(total_invoices),
        'total_paid': float(total_paid),
        'total_unpaid': float(total_unpaid),
        'revenue_month': float(revenue_month),
        'revenue_year': float(revenue_year),
        'overdue_count': int(overdue_count),
        'upcoming_due': int(upcoming_due),
        'trend': [
            {'month': int(row.month), 'revenue': float(row.revenue)}
            for row in trend_rows
        ],
        'top_clients': [
            {
                'client_id': int(row.client_id),
                'client_name': row.client_name,
                'revenue': float(row.revenue),
            }
            for row in top_clients_rows
        ],
        'recent_invoices': [
            {
                'id': int(row.id),
                'invoice_no': row.invoice_no,
                'status': str(row.status),
                'total': float(row.total or 0.0),
                'due_date': row.due_date,
            }
            for row in recent_invoices_rows
        ],
    }
