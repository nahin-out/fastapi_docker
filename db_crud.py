import os
from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv

ENV = os.getenv("APP_ENV", "local")

if ENV == "prod":
    load_dotenv(".env.prod")
else:
    load_dotenv(".env.local")
    
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_SERVER')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        