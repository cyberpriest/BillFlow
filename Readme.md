# InvoiceManager 🧾

> Build log & roadmap — check off each part as you go.

---

## What this app does

A multi-tenant invoicing tool. Each **User** owns one or more **Businesses**. Each business has **Clients**. Each client gets **Invoices**. Each invoice has **line items** that calculate the total automatically.

```
User → Business → Client → Invoice → InvoiceItem
```

---

## Auth System

This app uses **OTP-based auth** (no passwords on first login) + **JWT** for session.

### Flow

```
POST /auth/request-otp   →  user enters email, OTP sent
POST /auth/verify-otp    →  user enters OTP, JWT returned
```

JWT is then passed as `Authorization: Bearer <token>` on every protected route.

### Roles

| Role    | What they can do                          |
|---------|-------------------------------------------|
| `admin` | Full access — owns businesses, invites staff |
| `staff` | Access scoped to their assigned business  |

### Staff invite flow (already built ✅)

```
POST /admin/invite          →  admin sends OTP invite to staff email
POST /staff/register        →  staff sets name + password
POST /staff/verify          →  staff enters OTP → gets JWT
```

---

## Model Table

### User
| Column      | Type         | Notes                          |
|-------------|--------------|--------------------------------|
| id          | int PK       |                                |
| fullname    | str          | not unique                     |
| email       | str unique   |                                |
| password    | str nullable | set during staff registration  |
| role        | enum         | admin / staff                  |
| plan        | enum         | free / pro / etc               |
| shop_name   | str nullable |                                |
| created_at  | datetime     |                                |

---

### Business
| Column      | Type       | Notes                        |
|-------------|------------|------------------------------|
| id          | int PK     |                              |
| user_id     | FK → User  | owner                        |
| name        | str        | business/brand name          |
| email       | str        | contact email                |
| phone       | str        |                              |
| address     | str        |                              |
| currency    | str        | default: NGN                 |
| logo_url    | str nullable |                            |
| created_at  | datetime   |                              |

---

### Client
| Column          | Type          | Notes                   |
|-----------------|---------------|-------------------------|
| id              | int PK        |                         |
| business_id     | FK → Business |                         |
| name            | str           |                         |
| email           | str           |                         |
| phone           | str nullable  |                         |
| billing_address | str nullable  |                         |
| created_at      | datetime      |                         |

---

### Invoice
| Column      | Type          | Notes                              |
|-------------|---------------|------------------------------------|
| id          | int PK        |                                    |
| client_id   | FK → Client   |                                    |
| business_id | FK → Business | denormalised for easy filtering    |
| invoice_no  | str unique    | e.g. INV-0001                      |
| status      | enum          | draft / sent / paid / overdue      |
| issue_date  | date          |                                    |
| due_date    | date          |                                    |
| note        | str nullable  | optional message to client         |
| total       | float         | computed from InvoiceItems         |
| created_at  | datetime      |                                    |

---

### InvoiceItem
| Column      | Type          | Notes                        |
|-------------|---------------|------------------------------|
| id          | int PK        |                              |
| invoice_id  | FK → Invoice  |                              |
| description | str           | e.g. "Web design - 3 pages"  |
| quantity    | float         |                              |
| unit_price  | float         |                              |
| subtotal    | float         | quantity × unit_price        |

> `Invoice.total` = sum of all `InvoiceItem.subtotal` for that invoice.
> Compute this in a service function, not in the model.

---

## Roadmap

Work through this in order. Each section builds on the last.

### Phase 1 — Foundation ✅ (mostly done)
- [x] User model
- [x] OTP / invite system
- [x] JWT auth
- [x] Staff invite flow (request → register → verify)

---

### Phase 2 — Business & Client
- [ ] Business model + migrations
- [ ] `POST /businesses` — create a business (admin only)
- [ ] `GET /businesses` — list user's businesses
- [ ] `GET /businesses/{id}` — single business
- [ ] `PATCH /businesses/{id}` — update details
- [ ] Client model + migrations
- [ ] `POST /businesses/{id}/clients` — add client
- [ ] `GET /businesses/{id}/clients` — list clients
- [ ] `GET /clients/{id}` — single client
- [ ] `PATCH /clients/{id}` — update client

**Concepts you'll practice:** FK relationships, route nesting, ownership checks (does this business belong to the requesting user?)

---

### Phase 3 — Invoice CRUD
- [ ] Invoice model + InvoiceItem model + migrations
- [ ] `POST /clients/{id}/invoices` — create invoice (with items in body)
- [ ] `GET /clients/{id}/invoices` — list invoices
- [ ] `GET /invoices/{id}` — single invoice with items
- [ ] `PATCH /invoices/{id}` — update invoice / change status
- [ ] `DELETE /invoices/{id}` — delete (only if draft)
- [ ] Auto-calculate `Invoice.total` from items on create/update

**Concepts you'll practice:** nested create (invoice + items in one request), computed fields, conditional delete logic

---

### Phase 4 — Invoice Number Generation
- [ ] Auto-generate `invoice_no` (e.g. INV-0001, INV-0002) per business
- [ ] Make it sequential and padded

**Concepts you'll practice:** DB-level sequencing, scoped counters per business

---

### Phase 5 — Status & Business Logic
- [ ] `POST /invoices/{id}/send` — mark as sent (status: draft → sent)
- [ ] `POST /invoices/{id}/mark-paid` — mark as paid
- [ ] Overdue check — a background task or computed property that flags invoices past due_date as overdue

**Concepts you'll practice:** state machines, status transitions, background tasks (Celery)

---

### Phase 6 — Staff Scoping
- [ ] Staff can only see/create invoices for their assigned business
- [ ] Middleware or dependency to check: `current_user.business_id == resource.business_id`

**Concepts you'll practice:** role-based access control (RBAC), FastAPI dependencies

---

### Phase 7 — PDF Export (stretch goal)
- [ ] `GET /invoices/{id}/pdf` — generate and return a PDF of the invoice
- [x] Use `reportlab` (no GTK/native runtime required)

---

## Folder structure to aim for

```
app/
├── main.py
├── database.py
├── enums.py
├── auth.py
├── models/
│   ├── user.py
│   ├── business.py
│   ├── client.py
│   ├── invoice.py
├── schemas/
│   ├── user.py
│   ├── business.py
│   ├── client.py
│   ├── invoice.py
├── routers/
│   ├── auth.py
│   ├── admin.py
│   ├── businesses.py
│   ├── clients.py
│   ├── invoices.py
├── services/
│   ├── auth.py
│   ├── business.py
│   ├── client.py
│   ├── invoice.py
├── tasks.py
```

---

## Quick reference — things to remember

- Always use `lambda: datetime.now(tz=UTC)` for `default` on datetime columns, not `datetime.now(tz=UTC)` directly (it freezes at startup)
- `unique=True` on `fullname` will break — two people can share a name
- `shop_name` needs `nullable=True` or a default or it'll crash on staff creation
- `_invalidate_pending_invites` — use `synchronize_session="fetch"` on bulk deletes
- Return schema responses from endpoints, not raw model objects (don't leak OTP codes)
- Check ownership on every resource endpoint: does this business/client/invoice belong to `current_user`?

## Deployment / Railway

1. Commit everything to Git from the repo root.
2. Configure Railway to use the project root and set the build command to:

```bash
pip install -r requirements.txt
```

3. Set the start command in Railway to:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

4. Configure environment variables on Railway:
- `SECRET_KEY` (replace the default secret)
- `DATABASE_URL` (e.g. `sqlite:///test.db` for dev or a PostgreSQL URL for production)

5. If using SQLite on Railway, make sure the repository includes the file path you want to persist, but note SQLite is not ideal for production. Prefer PostgreSQL in Railway.
6. This project now uses `reportlab` for PDF generation, so Railway does not need the GTK/native WeasyPrint runtime.

> If you later switch back to `weasyprint`, you will need the native rendering libs on Linux.
