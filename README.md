# POS API

A FastAPI + SQLAlchemy point-of-sale backend with JWT auth, role-based
access control, and stock/payment integrity checks.

## Setup

```bash
python -m venv venv
source venv/bin/activate       
pip install -r requirements.txt
cp .env.example .env           
```

By default the app uses a local SQLite file (`pos.db`) so it runs with zero
extra setup. To use Postgres instead, set `DATABASE_URL` in `.env`, e.g.:

```
DATABASE_URL=postgresql://user:password@localhost:5432/pos_db
```

## Run

```bash
uvicorn app.main:app --reload
```

Docs at `http://localhost:8000/docs`.

## Creating the first admin

Public registration (`POST /auth/register`) always creates a `cashier`
account it can never grant elevated roles, even if `role` is included in
the request body. That's intentional: it closes off self-service privilege
escalation. To create the first admin:

```bash
python -m app.scripts.create_admin <username> <email> <password>
```

From there, an admin can promote other users via `PUT /users/{id}`.

## Roles

- **cashier** : can create sales, take payments, register customers
- **manager** : cashier permissions + manage products/categories/suppliers, approve refunds
- **admin** : everything, including managing user accounts/roles

## Security notes

- Passwords are hashed with bcrypt (via passlib) — plaintext is never stored.
- JWT access tokens (HS256), configurable expiry via `ACCESS_TOKEN_EXPIRE_MINUTES`.
- `/auth/login` has in-memory brute-force lockout (5 failed attempts / 15 min
  by default). For a multi-process deployment, swap this for a shared store
  (Redis) — see the comment in `app/services/auth_service.py`.
- Every write endpoint is behind role checks (`app/core/deps.py::require_roles`).
- Payments can never exceed a sale's remaining balance; refunds/status
  changes are restricted to admin/manager.
- Sales validate stock and decrement it atomically within the request; see
  the comment in `app/services/sale_service.py` about adding row locking
  (`SELECT ... FOR UPDATE`) if you move to Postgres under real concurrency.
- No stack traces or internals are ever returned to the client (global
  exception handler in `app/main.py`).
- `SECRET_KEY` must be set explicitly in production (`.env` / environment) 
  the fallback is a random value that changes every restart.

## Tests

Run the full suite locally:

```bash
pip install -r requirements.txt   # if you haven't already
pytest -v
```

No extra setup needed: tests run against an isolated **in-memory SQLite**
database created fresh for every test function (see `tests/conftest.py`
and `tests/test_*.py`). They never touch your real `pos.db` file or a
configured Postgres instance, and `DATABASE_URL` has no effect on them.

Coverage includes, for every major entity (auth, users, categories,
suppliers, customers, products, sales, sale items, payments, receipts):
successful CRUD operations, validation errors (422s), missing-resource
errors (404s), and role-based access failures (401/403s), plus the
sale/payment business rules (stock checks, overpayment rejection, refund
permissions) and the login lockout.

### Continuous Integration

Every push and pull request automatically runs the same suite via GitHub
Actions (`.github/workflows/tests.yml`)  checkout, set up Python 3.10,
`pip install -r requirements.txt`, then `pytest -v`. A red X on a PR means
a test failed; check the "Tests" workflow run for details.