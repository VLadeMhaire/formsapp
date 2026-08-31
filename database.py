import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Reads a .env file in the project root (if present) and loads its variables
# into the environment, so DATABASE_URL doesn't need to be set manually every
# time you open a new terminal.
load_dotenv()

# On Render/Railway/Neon/Supabase this comes from an env var you set in the
# dashboard. Locally, fall back to a local Postgres instance.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/forms",
)

# Neon/Supabase URLs sometimes start with "postgres://" or "postgresql://" —
# SQLAlchemy needs the driver named explicitly for psycopg3.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
