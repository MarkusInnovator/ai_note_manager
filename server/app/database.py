from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://testuser:testpass@localhost:5432/testdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
