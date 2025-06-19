from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'db.sqlite3')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from .models import User
    from passlib.hash import bcrypt
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Prepopulate admin and viewer if not exist
    if not db.query(User).filter_by(username='admin').first():
        admin = User(username='admin', hashed_password=bcrypt.hash('admin123'), role='admin')
        db.add(admin)
    if not db.query(User).filter_by(username='user').first():
        viewer = User(username='user', hashed_password=bcrypt.hash('user123'), role='viewer')
        db.add(viewer)
    db.commit()
    db.close() 