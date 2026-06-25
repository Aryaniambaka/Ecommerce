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


def test_get_current_user(auth_client, fixtureuser, session):
    response = auth_client.get("/current")
    data = response.json()
    schemavalidate = schemas.Current_user_detail(**data)
    assert response.status_code == 200
    assert fixtureuser["id"] == data["id"], "Error in test_get_current_user(id)"
    session.close()


def test_current_user_unauthorized(fixtureuser, client, session):
    response = client.get("/current")

    assert response.status_code == 401  # No Auth
    session.close()


@pytest.mark.parametrize("email,password", [
    ("lol@gmail.com", "string123"),
    ("lol1@gmail.com", "123")
])
def test_auth(client, email, password, session):
    form_data = {
        "username": email, "password": password
    }
    response = client.post("/login/verification", data=form_data)
    assert response.status_code == 403
    session.close()


def test_auth1(client, singleuser, session):
    form_data = {
        "username": singleuser["email"], "password": singleuser["password"]
    }

    response = client.post("login/verification", data=form_data)
    db_password = session.query(model.User).filter(model.User.email == singleuser["email"]).first().password
    lol = utility.verify_hashed_password(singleuser["password"], db_password)

    assert lol == True
    assert response.status_code == 200
    session.close()


def test_forgotpasswordf(S_auth_client, session):
    response = S_auth_client.post("user/forgotpassword")
    assert response.status_code == 422  # pydantic error
    session.close()


def test_forgotpasswordp(S_auth_client, session):
    data = {"email": "aryankumar4sep@gmail.com"}
    response = S_auth_client.post("user/forgotpassword", json=data)
    assert response.status_code == 200
    session.close()


def test_deleteuser(S_auth_client, session):
    response = S_auth_client.delete("user/delete/6969696")
    assert response.status_code == 404
    session.close()


def test_deleteuserp(S_auth_client, session):
    token = S_auth_client.cookies.get("access_token")
    payload = jwt.decode(
        token,
        config.settings.SECRET_KEY_1,
        algorithms=config.settings.ALGORITHM_1

    )
    user_id = payload["id"]
    response = S_auth_client.delete(f"user/delete/{user_id}")
    assert response.status_code == 200
    session.close()


def test_adduserprofile(S_auth_client, session):
    to_write = {
        "name": "aryan",
        "address": "O-609,OXY HOMEZ",
        "pincode": "201005"
    }
    response = S_auth_client.post("/user/add_profile", json=to_write)
    assert response.json()["message"] == "profile creation is success"
    assert response.status_code == 201
    session.close()


def test_adduserprofilef(S_auth_client, session):
    to_write = {
        "name": "aryan",
        "address": "O-609,OXY HOMEZ",

    }
    response = S_auth_client.post("/user/add_profile", json=to_write)
    assert response.status_code == 422
    session.close()


def test_verify_otp(S_auth_client, session):
    to_write={"email":"aryankumar4sep@gmail.com"}

    response=S_auth_client.post("user/forgotpassword",json=to_write)
    assert response.status_code==200





    otp = session.query(model.Forgot_password).filter().order_by(desc(model.Forgot_password.time)).first().otp


    to_data = {
        "otp": otp,
        "email": "aryankumar4sep@gmail.com",
        "newpassword":"lol"
    }
    response = S_auth_client.patch("/user/verifyotp", json=to_data)
    assert response.status_code == 200
    assert response.json()["message"]=="password reset successfully"
    session.close()
def test_verify_otpfail(S_auth_client, session):
    to_write={"email":"aryankumar4sep@gmail.com"}

    response=S_auth_client.post("user/forgotpassword",json=to_write)
    assert response.status_code==200





    otp = session.query(model.Forgot_password).filter().order_by(desc(model.Forgot_password.time)).first().otp

    to_data = {
        "otp": "999999",
        "email": "aryankumar4sep@gmail.com",
        "newpassword":"lol"
    }
    response = S_auth_client.patch("/user/verifyotp", json=to_data)
    assert response.status_code == 400
    assert response.json()["detail"]=="Invalid or expired OTP"
    session.close()

@freeze_time("2026-06-24 12:00:00")
def test_verify_otptimeout(S_auth_client, session):
    to_write = {"email": "aryankumar4sep@gmail.com"}

    response = S_auth_client.post("user/forgotpassword", json=to_write)
    assert response.status_code == 200

    otp = session.query(model.Forgot_password).filter().order_by(desc(model.Forgot_password.time)).first().otp

    to_data = {
        "otp": otp,
        "email": "aryankumar4sep@gmail.com",
        "newpassword": "lol"
    }
    with freeze_time("2026-06-24 12:11:00"):
        response = S_auth_client.patch("/user/verifyotp", json=to_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid or expired OTP"
    session.close()
def test_patchprofile(S_auth_client,session):
    to_write = {
        "name": "aryan",
        "address": "O-609,OXY HOMEZ",
        "pincode": "201005"
    }
    response = S_auth_client.post("/user/add_profile", json=to_write)
    assert response.json()["message"] == "profile creation is success"
    assert response.status_code == 201
    to_update={
        "name":"Dr jhatka"
    }
    response2=S_auth_client.patch("/user/updateprofile/me", json=to_update)
    assert response2.status_code==200
    assert response2.json()["message"]=="Profile updated successfully"
    session.close()

