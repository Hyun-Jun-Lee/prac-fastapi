from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from core.config import settings


engine = create_engine(settings.DB_URL, pool_recycle=500)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
