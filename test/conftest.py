from fastapi.testclient import TestClient #acts like browser
from fastapi import status
from app.main import app
from app.database import Base,get_db
from test.db import session
from app import schemas,Oauth2,model,utility

import pytest
@pytest.fixture
def client(session):
    def override_db():
        yield session
    app.dependency_overrides[get_db]=override_db
    yield TestClient(app)
    app.dependency_overrides.clear()
@pytest.fixture
def client2(session):# always create different client for each fixture if mutiple has same client so only lastest cookies left so ecah client each browser
    def override_db():
        yield session
    app.dependency_overrides[get_db]=override_db
    yield TestClient(app)
    app.dependency_overrides.clear()
@pytest.fixture(params=[
    ("test1@gmail.com","string"),
    ("test2@gmail.com","string"),
    ("aryankumar4sep@gmail.com","string")
])
def fixtureuser(client,request):
    email,password=request.param
    credential={"email":email,"password":password}
    response=client.post("/user/login/create",json=credential)
    user=response.json()
    assert response.status_code == 201
    assert user["email"]==credential["email"],"error in accessing db"
    newuser=schemas.SuccessLoginReturn(**response.json())#converts to object
    return user

@pytest.fixture
def token_generate(fixtureuser):
    return Oauth2.create_access_token({"id":fixtureuser["id"],"email":fixtureuser["email"]})

@pytest.fixture
def auth_client(client,token_generate):
    client.cookies.set("access_token",token_generate)
    return client
@pytest.fixture(params=[

    ("aryankumar4sep@gmail.com","string")
])
def singleuser(client,request):
    email,password=request.param
    credential={"email":email,"password":password}
    response=client.post("/user/login/create",json=credential)
    user=response.json()
    user["password"] = password
    assert response.status_code == 201
    assert user["email"]==credential["email"],"error in accessing db"
    newuser=schemas.SuccessLoginReturn(**response.json())#converts to object
    return user
@pytest.fixture
def token_generateS(singleuser):
    return Oauth2.create_access_token({"id":singleuser["id"],"email":singleuser["email"]})
@pytest.fixture
def S_auth_client(client,token_generateS):
    client.cookies.set("access_token",token_generateS)
    return client

@pytest.fixture(params=[

    ("aryankumar4sep+seller@gmail.com","string")
])
def seller(client2,request):
    email,password=request.param
    credential={"email":email,"password":password}
    response=client2.post("/seller/login/create",json=credential)
    user=response.json()
    user["password"] = password
    assert response.status_code == 201
    assert user["email"]==credential["email"],"error in accessing db"
    newuser=schemas.SuccessLoginReturn(**response.json())#converts to object
    return user
@pytest.fixture
def token_generateseller(seller):
    return Oauth2.create_access_token({"id":seller["id"],"email":seller["email"]})
@pytest.fixture
def Seller_auth_client(client2,token_generateseller):
    client2.cookies.set("access_token",token_generateseller)
    return client2
