from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.config import settings
from app.database import Base,get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine=create_engine(settings.TEST_DB)
TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()





