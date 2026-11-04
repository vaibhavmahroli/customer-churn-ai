from src.database import engine, Base
from src import models

# Create all database tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")