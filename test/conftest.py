
from fastapi.testclient import TestClient #acts like browser
from fastapi import status
from app.main import app
from app.database import Base,get_db
from test.db import session
from app import schemas,Oauth2
import pytest
@pytest.fixture
def client(session):
    def over_ride_get_db():
        yield session
    app.dependency_overrides[get_db]=over_ride_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
@pytest.fixture(params=[
    ("test1@gmail.com","string1"),
    ("test2@gmail.com","string2"),
    ("test3@gmail.com","string3")
])
def fixtureuser(client,request):
    email,password= request.param
    credentials={"email":email,"password":password}
    response=client.post("/user/login/create",json=credentials)
    user=response.json()
    assert response.status_code == 201

    assert user["email"]==credentials["email"],"error in accessing db[2]"
    newuser= schemas.SuccessLoginReturn(**response.json())


    return user
@pytest.fixture
def get_token(fixtureuser):
    return Oauth2.create_access_token({"id":fixtureuser["id"],"email":fixtureuser["email"]})
@pytest.fixture
def authorized_client(client,get_token):
    client.cookies.set("access_token",get_token)
    return client










