import pytest
import time
from jose import jwt
from app import config
from sqlalchemy import desc

from test.db import session
from app import schemas,Oauth2,model,utility
from app import schemas
from freezegun import freeze_time
from datetime import datetime, timedelta
def test_get_current_seller(Seller_auth_client, seller, session):
    response = Seller_auth_client.get("/current")
    data = response.json()
    schemavalidate = schemas.Current_user_detail(**data)
    assert response.status_code == 200
    assert data["role"]=="seller"
    assert seller["id"] == data["id"], "Error in test_get_current_user(id)"
    session.close()

def test_addsellerprofile(Seller_auth_client, session):
    to_write = {

        "GSTNo": "07AAAAA1111A2Z1",
        "CompanyName": "Test Corp",
        "OwnerName": "Owner",
        "Address": "Addr",
        "Pincode": "123456"
    }
    response = Seller_auth_client.post("/seller/add_details", json=to_write)
    assert response.json()["message"]=='profile created succesfully'

    assert response.status_code == 201
    session.close()
def test_addsellerprofilefail(Seller_auth_client, session):
    to_write = {
        "name": "aryan",
        "address": "O-609,OXY HOMEZ",

    }
    response = Seller_auth_client.post("/seller/add_details", json=to_write)
    assert response.status_code == 422
    session.close()
def test_deletesellerp(Seller_auth_client, session):
    token = Seller_auth_client.cookies.get("access_token")
    payload = jwt.decode(
        token,
        config.settings.SECRET_KEY_1,
        algorithms=config.settings.ALGORITHM_1

    )
    seller_id = payload["id"]
    response = Seller_auth_client.delete(f"/seller/delete/{seller_id}")
    assert response.status_code == 200
    session.close()
def test_deletesellerfail(Seller_auth_client, session):

    response = Seller_auth_client.delete(f"/seller/delete/696969")
    assert response.status_code == 404
    session.close()
def test_updatesellerfailnotexits(Seller_auth_client, session):
    token = Seller_auth_client.cookies.get("access_token")
    payload = jwt.decode(
        token,
        config.settings.SECRET_KEY_1,
        algorithms=config.settings.ALGORITHM_1

    )# here there is no profile to update
    seller_id = payload["id"]
    to_update={
        "OwnerName":"Aryan"
    }
    response = Seller_auth_client.patch(f"/seller/updateprofile/{seller_id}",json=to_update)
    assert response.status_code==404
    assert response.json()["detail"]=="profile do not exits"
    session.close()
def test_updatesellerpass(Seller_auth_client, session):
    token = Seller_auth_client.cookies.get("access_token")
    payload = jwt.decode(
        token,
        config.settings.SECRET_KEY_1,
        algorithms=config.settings.ALGORITHM_1

    )

    seller_id = payload["id"]
    to_write = {

        "GSTNo": "07AAAAA1111A2Z1",
        "CompanyName": "Test Corp",
        "OwnerName": "Owner",
        "Address": "Addr",
        "Pincode": "123456"
    }
    response = Seller_auth_client.post("/seller/add_details", json=to_write)
    to_update={
        "OwnerName":"Aryan"
    }
    response = Seller_auth_client.patch(f"/seller/updateprofile/{seller_id}",json=to_update)
    assert response.status_code==200
    assert response.json()["message"]=="successfully updated"
    session.close()