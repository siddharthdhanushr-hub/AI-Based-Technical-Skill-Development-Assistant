import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
data_dir = os.path.join(project_root, "data")
os.makedirs(data_dir, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(data_dir, 'app.db')}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
