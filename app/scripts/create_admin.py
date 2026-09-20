"""
Bootstrap the first admin account.

Public registration (/auth/register) always creates a "cashier" account on
purpose - it can never grant elevated roles. So the very first admin has to
be created directly, either with this script or by an operator inserting a
row. Every admin after that can be promoted via PUT /users/{id}.

Usage:
    python -m app.scripts.create_admin <username> <email> <password>
"""
import sys

from app.core.security import hash_password
from app.database import Base, SessionLocal, engine
from app.models.user import User


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python -m app.scripts.create_admin <username> <email> <password>")
        raise SystemExit(1)

    username, email, password = sys.argv[1:4]

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).filter(User.username == username).first():
            print(f"User '{username}' already exists - nothing to do.")
            return

        admin = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print(f"Admin user '{username}' created.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
